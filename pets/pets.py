import streamlit as st
from pets import foodAndSupplyRecommendation, viewMyPets, vetLocator, chatbot

def show_navbar():
    st.markdown("""
        <style>
            .navbar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 1000;
                display: flex;
                background-color: #333;
            }
            .navbar button {
                flex: 1;
                background-color: #333;
                border: none;
                color: white;
                padding: 15px 0;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .navbar button:hover {
                background-color: #555;
            }
            .navbar button:active {
                background-color: #4CAF50;
            }
            .content {
                margin-top: 50px;
            }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state if not exists
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"

    # Navigation buttons with direct state updates
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Food & Supply", key="food_supply"):
            st.session_state['nav'] = "Food and Supply Recommendations"
            st.experimental_rerun()

    with col2:
        if st.button("View My Pets", key="view_pets"):
            st.session_state['nav'] = "View My Pets"
            st.experimental_rerun()

    with col3:
        if st.button("Vet Locator", key="vet_loc"):
            st.session_state['nav'] = "Vet Locator"
            st.experimental_rerun()

    with col4:
        if st.button("Chatbot", key="chat"):
            st.session_state['nav'] = "Chatbot"
            st.experimental_rerun()

def show_pets_navigation():
    # Initialize session state if not exists
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"

    # Render the sticky navbar
    show_navbar()

    # Display the selected feature based on session state
    if st.session_state['nav'] == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()
    elif st.session_state['nav'] == "View My Pets":
        viewMyPets.main()
    elif st.session_state['nav'] == "Vet Locator":
        vetLocator.vet_locator([3.1390, 101.6869])
    elif st.session_state['nav'] == "Chatbot":
        chatbot.show_feature()