import streamlit as st
from pets import pets
import animalIdentification

# Create two columns for layout
col1, col2 = st.columns([1, 3])  # Adjust the ratio for width (1:3 is an example)

# Left-side navigation
with col1:
    st.sidebar.title("Main Navigation")
    # Set default to "Home" by specifying index=2 (as "Home" is the 3rd option in the list)
    main_selection = st.sidebar.radio(
        "Select a Page", 
        ["Animal Identification", "Pets", "Home"], 
        index=2  # Set the default selection to "Home"
    )

# Right-side navigation (only appears if "Pets" is selected)
with col2:
    if main_selection == "Animal Identification":
        animalIdentification.animal_identification()
        

    elif main_selection == "Pets":
        pets.show_pets_navigation()

    else:
        st.title("Welcome to PetPedia")
        st.write("Select a page from the left sidebar.")
