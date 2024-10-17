import sqlite3
import streamlit as st
from PIL import Image
from io import BytesIO
from openai import OpenAI  # Ensure you have the OpenAI package installed


client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Function to edit image using DALL-E
def edit_image_with_dalle(image):
    image.seek(0)  # Ensure the stream is at the start
    try:
        response = client.image.edit(
            image=image,
            instructions="Create a vivid style picture similar to this one."
        )
        return response['data']['url']
    except Exception as e:
        st.error(f"Error using DALL-E: {e}")
        return ""

# Function to insert pet data into SQLite database
def insert_pet_data(pet_type, age, breed, personality, health_condition, image_url):
    conn = sqlite3.connect('PetPedia.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO pets (pet_type, age, breed, personality, health_condition, image_url)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (pet_type, age, breed, personality, health_condition, image_url))
    conn.commit()
    conn.close()

# Streamlit form to collect pet details
def show_pet_form():
    st.title("Add Pet Information")

    pet_type = st.selectbox("Pet Type", ["Dog", "Cat", "Bird", "Other"])
    if pet_type == "Other":
        pet_type = st.text_input("Specify Pet Type")

    age = st.number_input("Age", min_value=0)
    breed = st.text_input("Breed")
    personality = st.selectbox("Personality", ["Playful and Energetic", "Calm and Relaxed", "Intelligent and Observant", "Fearful and Anxious", "Social and Outgoing", "Other"])
    if personality == "Other":
        personality = st.text_input("Specify Personality")

    health_condition = st.text_area("Health Condition", value="healthy")

    # Image upload feature
    uploaded_image = st.file_uploader("Upload Pet Image", type=["png", "jpg", "jpeg"])

    if st.button("Submit"):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            file_stream = BytesIO()
            image.save(file_stream, format='PNG')
            file_stream.seek(0)  # Reset stream position

            # Generate the image URL using DALL-E API
            image_url = edit_image_with_dalle(file_stream)

            if image_url:
                # Insert all details into the database
                insert_pet_data(pet_type, age, breed, personality, health_condition, image_url)
                st.success("Pet information saved successfully!")
            else:
                st.error("Image generation failed.")
        else:
            st.error("Please upload an image.")

# Fetch and display pet data
def fetch_pet_data():
    conn = sqlite3.connect('PetPedia.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM pets')
    rows = cur.fetchall()
    conn.close()
    return rows

# Streamlit app to display pet data
def show_pet_data():
    st.title("Pet Information")
    pet_data = fetch_pet_data()

    if pet_data:
        for row in pet_data:
            st.markdown(f"## Pet ID: {row[0]}")
            st.markdown(f"### Type: {row[1]}")
            st.markdown(f"**Age**: {row[2]} years")
            st.markdown(f"**Breed**: {row[3]}")
            st.markdown(f"**Personality**: {row[4]}")
            st.markdown(f"**Health Condition**: {row[5]}")

            # Display pet image
            if row[6]:
                st.image(row[6], caption=f"{row[1]} Image")
            st.write("---")
    else:
        st.write("No pet data found.")

# Create a table to store pet details, including image URLs
def create_table():
    conn = sqlite3.connect('PetPedia.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY,
        pet_type TEXT,
        age INTEGER,
        breed TEXT,
        personality TEXT,
        health_condition TEXT,
        image_url TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Main application
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add Pet", "View Pets"])

    create_table()  # Ensure table is created

    if page == "Add Pet":
        show_pet_form()
    elif page == "View Pets":
        show_pet_data()

if __name__ == "__main__":
    main()
