# import streamlit as st
# import openai
# import google.generativeai as genai
# import PIL.Image

# # Configure OpenAI and GeminiAI API keys
# openai.api_key = st.secrets["OpenAI_API_Key"]
# genai.configure(api_key=st.secrets["GeminiAI_API_Key"])

# def animal_identification():
#     st.title("Animal Breed & Species Identifier")

#     # Let the user upload an image file
#     uploaded_file = st.file_uploader("Upload an image of an animal", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         # Open the image using PIL
#         image = PIL.Image.open(uploaded_file)

#         # Display the uploaded image
#         st.image(image, caption="Uploaded Image", use_column_width=True)

#         # Define the generative model
#         model = genai.GenerativeModel(
#             "gemini-1.5-flash",
#             system_instruction="""
#             You are an animal expert that is able to identify the breed and the species of the given image.
#             You are also able to give a brief description of the animal. The output must be in the below format:
#             Breed: <breed>
#             Species: <species>
#             Characteristics: <characteristics>
#             Diet: <diet>
#             Lifespan: <lifespan>
#             Habitat: <habitat>
#             Description: <description>
#             """
#         )

#         # Call the generative model with the image
#         response = model.generate_content(["Identify the breed and the species of the given image.", image])

#         # Display the model's response
#         st.subheader("Identification Result")
#         st.text(response.text)

