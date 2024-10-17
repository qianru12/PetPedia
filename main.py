import streamlit as st
from pets import pets
import animalIdentification
import test

# Updated CSS for radio buttons and circular image
st.markdown("""
<style>
    /* Radio button styling */
    .stRadio [role=radiogroup] {
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .stRadio [role=radiogroup] label {
        background-color: #f0f2f6;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        width: 100%;
    }

    .stRadio [role=radiogroup] label:hover {
        background-color: #e0e2e6;
    }

    .stRadio [role=radiogroup] label[data-checked=true] {
        background-color: #4CAF50 !important;
        color: white !important;
    }

    /* Hide the default radio button */
    .stRadio [role=radiogroup] input {
        clip: rect(0 0 0 0);
        clip-path: inset(50%);
        height: 1px;
        overflow: hidden;
        position: absolute;
        white-space: nowrap;
        width: 1px;
    }

    /* Circular image styling */
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

