from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Image Translator")

st.markdown("""
<h1 style="color: #3498db; text-align: center;">Image Translator</h1>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image to translate...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
st.markdown("""
<style>
.stApp {
  background-color: #e8f4f8;
}
.stButton > button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.stButton > button:hover {
  background-color: #2980b9;
}
</style>
""", unsafe_allow_html=True)
submit=st.button("Translate Image")

input_prompt="""
you are an expert translator , who can translate any language to best english, you are very good in english, kannada and malayalam 
Translate the text in the image to English.
"""


if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,"")
    st.subheader("Translation:")
    st.write(response)