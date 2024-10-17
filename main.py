import streamlit as st
from pets import pets
import animalIdentification
import test

# Custom CSS for radio buttons and circular image
st.markdown("""
<style>
    /* Existing radio button styles */
    div.row-widget.stRadio > div {
        flex-direction: column;
        align-items: stretch;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        padding: 10px 15px;
        margin: 4px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        text-align: center;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: #555;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #4CAF50;
        color: white;
    }
    div.row-widget.stRadio > div[role="radiogroup"] input[type="radio"] {
        position: absolute;
        opacity: 0;
        width: 0;
        height: 0;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* New circular image styles */
    .circular-image {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        object-fit: cover;
        display: block;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 3])

# Left-side navigation
with col1:
    st.sidebar.title("Main Navigation")
    main_selection = st.sidebar.radio(
        "Select a Page", 
        ["Animal Identification", "Pets", "Home"], 
        index=2
    )

with col2:
    if main_selection == "Animal Identification":
        animalIdentification.main()
    elif main_selection == "Pets":
        pets.show_pets_navigation()
    elif main_selection == "Home":
        st.title("Welcome to PetPedia")
        image = "image_2024-10-16_10-49-09.png"
        st.image(image, width=600)  
        
        st.write("Select a page from the left sidebar.")

