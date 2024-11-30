from dotenv import load_dotenv

load_dotenv() 

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if not input and not image:
        st.warning("Please provide either an input prompt or an image.", icon="⚠️")
        return None
    
    if not image:
        response = model.generate_content(input)
    elif not input:
        response = model.generate_content(["tell me about the image",image])
    else:
        response = model.generate_content([input, image])
    
    return response.text if response else "No response received."

st.set_page_config(page_title="question and answer")
st.header("Gemini")

input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("ask question")

if submit:
    response = get_gemini_response(input, image)
    st.write(response)