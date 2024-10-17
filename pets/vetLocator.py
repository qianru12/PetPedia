import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os

API_KEY = os.getenv('GOOGLE_API_KEY')

def get_vet_clinics(lat, lng, radius=10000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=veterinary_care&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("results", [])

        if not results:
            st.warning("No vet clinics found in the area. Expanding search to include all types of places...")
            url_fallback = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&key={API_KEY}"
            fallback_response = requests.get(url_fallback)
            if fallback_response.status_code == 200:
                fallback_results = fallback_response.json().get("results", [])
                return fallback_results
            else:
                st.error("Error retrieving fallback results.")
                return []

        vet_clinics = []
        for result in results:
            clinic = {
                'name': result.get('name', 'Name not available'),
                'location': [result['geometry']['location']['lat'], result['geometry']['location']['lng']],
                'address': result.get('vicinity', 'Address not available'),
                'status': result.get('business_status', 'Status not available')
            }
            vet_clinics.append(clinic)
        return vet_clinics
    else:
        st.error(f"Error retrieving vet clinics: {response.status_code}")
        return []

def vet_locator(initial_location):
    st.title("Vet Clinic Locator")

    if 'user_location' not in st.session_state:
        st.session_state.user_location = initial_location

    if 'show_vet_map' not in st.session_state:
        st.session_state.show_vet_map = False

    st.write("Drag the marker on the map to set your location, and click 'Confirm Location'.")

    # First map: Create the initial map with a draggable marker for location selection
    m = folium.Map(location=st.session_state.user_location, zoom_start=12)
    marker = folium.Marker(location=st.session_state.user_location, popup="Drag me!", draggable=True)
    marker.add_to(m)

    # Display the first map with a draggable marker
    output = st_folium(m, width=700, height=500)

    # Check if the user has moved the marker
    if output and output['last_clicked']:
        st.session_state.user_location = [output['last_clicked']['lat'], output['last_clicked']['lng']]

    # Show the selected location
    user_lat, user_lng = st.session_state.user_location
    st.write(f"Selected location: Latitude {user_lat}, Longitude {user_lng}")

    # Add a "Confirm Location" button for the user to confirm the selected location
    if st.button('Confirm Location'):
        # Set the flag in session state to show the second map
        st.session_state.show_vet_map = True

    # Conditionally render the second map if the "Confirm Location" button was clicked
    if st.session_state.show_vet_map:
        vet_results = get_vet_clinics(user_lat, user_lng)

        # Second map: Create a new map centered at the updated location
        new_map = folium.Map(location=[user_lat, user_lng], zoom_start=13)

        # Add the exact same user's location marker from the first map to the second map
        folium.Marker(location=[user_lat, user_lng], popup="Your Location", icon=folium.Icon(color="blue")).add_to(new_map)

        # Add markers for each retrieved vet clinic to the second map
        for vet in vet_results:
            name = vet.get('name', 'Name not available')
            address = vet.get('address', 'Address not available')
            status = vet.get('status', 'Status not available')
            popup_text = f"{name}\nStatus: {status}\nAddress: {address}"
            folium.Marker(location=vet['location'], popup=popup_text, icon=folium.Icon(color="green")).add_to(new_map)

        # Display the updated second map with clinic markers
        st.write("Map with vet clinics:")
        st_folium(new_map, width=700, height=500)

        # Display the vet clinic details below the second map
        st.subheader("Nearby Vet Clinics:")
        for vet in vet_results:
            st.write(f"*Name*: {vet.get('name', 'Name not available')}")
            st.write(f"*Status*: {vet.get('status', 'Status not available')}")
            st.write(f"*Address*: {vet.get('address', 'Address not available')}")
            st.write("---")
    else:
        st.write("Confirm your location to see nearby vet clinics.")

vet_locator([3.1390, 101.6869])