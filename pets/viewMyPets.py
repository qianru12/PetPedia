import streamlit as st
from openai import OpenAI
import google.generativeai as genai
from PIL import Image
import io
import sqlite3

# Configure API clients
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

# Function to create description using Gemini
def create_description(image):
    image_pil = Image.open(image)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(["Describe in detail the animal in this image", image_pil])
    return response.text

# Function to edit image using DALL-E
def create_image_from_description(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Function to insert pet data into SQLite database
def insert_pet_data(name, pet_type, age, breed, personality, health_condition, image_url):
    conn = sqlite3.connect('PetPedia.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO pets (name, pet_type, age, breed, personality, health_condition, image_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, pet_type, age, breed, personality, health_condition, image_url))
    conn.commit()
    conn.close()

# Streamlit form to collect pet details
def show_pet_form():
    st.title("Add Pet Information")

    name = st.text_input("Pet Name")
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
            description = create_description(uploaded_image)
            prompt = f"Based on this description: {description}, create an avatar for this animal."
            image_url = create_image_from_description(prompt)

            if image_url:
                # Insert all details into the database
                insert_pet_data(name, pet_type, age, breed, personality, health_condition, image_url)
                st.success("Pet information saved successfully!")
                st.image(image_url, caption="Generated Pet Avatar")
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

def analyze_pet_data():
    pet_data = fetch_pet_data()
    if not pet_data:
        return "No pet data available for analysis."

    pet_info = ", ".join([f"Pet Type: {row[2]}, Age: {row[3]}, Breed: {row[4]}, Personality: {row[5]}, Health Condition: {row[6]}" for row in pet_data])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""Pet information: {pet_info}. According to the information provided, generate a comprehensive care guide for these pets based on their characteristics. The guide should include detailed information on the following aspects:
Feeding: Frequency, portion size, recommended diet types, and potential dietary restrictions.
Exercise: Daily requirements, suitable activities, and considerations for different ages and energy levels.
Grooming: Frequency, necessary tools, and specific grooming techniques for the pets' coat types.
Training: Basic obedience commands, socialization methods, and potential behavioral challenges.
Health: Common health issues, preventative measures, and recommended vaccination schedule.
Environmental Enrichment: Ideas for stimulating mental and physical well-being.
Socialization: Importance of early socialization, opportunities, and potential challenges.""")
    return response.text

# Streamlit app to display pet data
def show_pet_data():
    st.title("Pet Information")
    pet_data = fetch_pet_data()

    if pet_data:
        for row in pet_data:
            if row[7]:  # image_url is now at index 7
                st.image(row[7], caption=f"{row[1]} Avatar")  # row[1] is now the name
            st.write("---")
            st.markdown(f"## Pet ID: {row[0]}")
            st.markdown(f"### Name: {row[1]}")
            st.markdown(f"### Type: {row[2]}")
            st.markdown(f"**Age**: {row[3]} years")
            st.markdown(f"**Breed**: {row[4]}")
            st.markdown(f"**Personality**: {row[5]}")
            st.markdown(f"**Health Condition**: {row[6]}")

            st.write("---")

        # Display the analysis after listing all pets
        st.subheader("Pet Care Analysis")
        analysis = analyze_pet_data()
        st.write(analysis)
    else:
        st.write("No pet data found.")

# Create a table to store pet details, including image URLs
def create_table():
    conn = sqlite3.connect('PetPedia.db')
    cur = conn.cursor()

    # Create the new table with the 'name' field
    cur.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY,
        name TEXT,
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