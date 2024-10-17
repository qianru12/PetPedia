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
        .navbar button.active {
            background-color: #4CAF50;
        }
        .content {
            margin-top: 50px;
        }
    </style>

    <div class="navbar">
        <button onclick="setNav('Food and Supply Recommendations')" id="btn1">Food & Supply</button>
        <button onclick="setNav('View My Pets')" id="btn2">View My Pets</button>
        <button onclick="setNav('Vet Locator')" id="btn3">Vet Locator</button>
        <button onclick="setNav('Chatbot')" id="btn4">Chatbot</button>
    </div>

    <script>
    function setNav(value) {
        localStorage.setItem('nav', value);
        updateButtonStates(value);
        window.dispatchEvent(new Event('storage'));
    }

    function updateButtonStates(value) {
        const buttons = document.querySelectorAll('.navbar button');
        buttons.forEach(button => {
            button.classList.remove('active');
            if (button.textContent === value) {
                button.classList.add('active');
            }
        });
    }

    document.addEventListener('DOMContentLoaded', (event) => {
        const nav = localStorage.getItem('nav') || 'Food and Supply Recommendations';
        updateButtonStates(nav);
    });
    </script>

    <div class="content"></div>
    """, unsafe_allow_html=True)

def show_pets_navigation():
    show_navbar()

    # Use session_state to store the navigation state
    if 'nav' not in st.session_state:
        st.session_state['nav'] = "Food and Supply Recommendations"

    # JavaScript to update Streamlit session state
    st.markdown("""
    <script>
    window.addEventListener('storage', function(e) {
        const nav = localStorage.getItem('nav');
        if (nav) {
            Streamlit.setComponentValue('nav', nav);
        }
    });
    </script>
    """, unsafe_allow_html=True)

    # Update session state based on JavaScript events
    nav = st.text_input('nav', value='', key='nav', label_visibility='hidden')
    if nav:
        st.session_state['nav'] = nav

    # Display the selected feature
    if st.session_state['nav'] == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()
    elif st.session_state['nav'] == "View My Pets":
        viewMyPets.main()
    elif st.session_state['nav'] == "Vet Locator":
        vetLocator.vet_locator([3.1390, 101.6869])
    elif st.session_state['nav'] == "Chatbot":
        chatbot.show_feature()