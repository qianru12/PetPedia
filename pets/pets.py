import streamlit as st
from pets import foodAndSupplyRecommendation, viewMyPets, vetLocator, chatbot

def show_navbar():
    # Custom CSS and HTML for the navigation bar
    st.markdown("""
        <style>
            /* Header styling */
            .stApp > header {
                background-color: transparent;
            }

            /* Navigation bar container */
            .custom-navbar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 999;
                display: flex;
                justify-content: space-between;
                padding: 1rem;
                background-color: #333;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            /* Navigation buttons */
            .nav-button {
                background-color: #333;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                margin: 0 0.25rem;
                cursor: pointer;
                border-radius: 4px;
                transition: background-color 0.3s;
                flex: 1;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
            }

            .nav-button:hover {
                background-color: #555;
            }

            .nav-button.active {
                background-color: #4CAF50;
            }

            /* Main content spacing */
            .main-content {
                margin-top: 4rem;
                padding: 1rem;
            }

            /* Hide Streamlit's default header */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}

            /* Adjustments for mobile */
            @media (max-width: 768px) {
                .nav-button {
                    padding: 0.5rem;
                    font-size: 14px;
                }
            }
        </style>
        """, unsafe_allow_html=True)

    # Create the navigation bar using HTML
    nav_html = f"""
    <div class="custom-navbar">
        <div class="nav-button {'active' if st.session_state.get('nav') == 'Food and Supply Recommendations' else ''}" 
             onclick="window.location.href='?nav=food'">Food & Supply</div>
        <div class="nav-button {'active' if st.session_state.get('nav') == 'View My Pets' else ''}" 
             onclick="window.location.href='?nav=pets'">View My Pets</div>
        <div class="nav-button {'active' if st.session_state.get('nav') == 'Vet Locator' else ''}" 
             onclick="window.location.href='?nav=vet'">Vet Locator</div>
        <div class="nav-button {'active' if st.session_state.get('nav') == 'Chatbot' else ''}" 
             onclick="window.location.href='?nav=chat'">Chatbot</div>
    </div>
    <div class="main-content"></div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

    # Handle navigation based on URL parameters
    params = st.experimental_get_query_params()
    nav_param = params.get('nav', ['food'])[0]

    if nav_param == 'food':
        st.session_state['nav'] = "Food and Supply Recommendations"
    elif nav_param == 'pets':
        st.session_state['nav'] = "View My Pets"
    elif nav_param == 'vet':
        st.session_state['nav'] = "Vet Locator"
    elif nav_param == 'chat':
        st.session_state['nav'] = "Chatbot"

def show_pets_navigation():
    # Initialize session state
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"

    # Render the navbar
    show_navbar()

    # Add spacing for the fixed navbar
    st.markdown("<div style='margin-top: 70px;'></div>", unsafe_allow_html=True)

    # Display the selected feature
    if st.session_state['nav'] == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()
    elif st.session_state['nav'] == "View My Pets":
        viewMyPets.main()
    elif st.session_state['nav'] == "Vet Locator":
        vetLocator.vet_locator([3.1390, 101.6869])
    elif st.session_state['nav'] == "Chatbot":
        chatbot.show_feature()