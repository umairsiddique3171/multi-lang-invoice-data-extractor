# importing dependencies
from dotenv import load_dotenv
load_dotenv() # loading .env variable as environment variables in current session

import os 
from PIL import Image
import streamlit as st
import google.generativeai as genai
from utils import set_background

# configuration with api_key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# func to load GeminiProVision and get response
model = genai.GenerativeModel("gemini-pro-vision")
def get_gemini_response(input,image_data,input_prompt):
    if image_data:
        response = model.generate_content([input, image_data[0], input_prompt])
        return response.text
    return "No image data provided"

# initial streamlit app
st.set_page_config(page_title="Multi-Language Invoice Data Extractor")
st.header("Multi-Language Invoice Data Extractor")

# set background
set_background('background_img.jpg')

# inputs
input_prompt = st.text_input("#### Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an Invoice Image",type=['jpg','png','jpeg'])
image = ""
if uploaded_file is not None: 
    image = Image.open(uploaded_file)
    # show invoice image
    st.image(image,caption="Uploaded Image",use_column_width=True)



submit = st.button("Submit")

prompt = """
I will upload an invoice image and I want you to answer the question based on that invoice image
"""
def image_processing(uploaded_file):
    if uploaded_file is not None: 
        bytes_data = uploaded_file.getvalue()
        image_parts=[
            {
            "mime_type": uploaded_file.type,# Multipurpose Internet Mail Extension
            "data":bytes_data
            }
        ]
        return image_parts
    else: 
        raise FileNotFoundError("file is not uploaded...")

if submit : 
    image_data = image_processing(uploaded_file=uploaded_file)
    response = get_gemini_response(prompt,image_data,input_prompt)
    st.subheader("Response: ")
    st.write(response)


                                            