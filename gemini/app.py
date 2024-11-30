from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model= genai.GenerativeModel("gemini-1.5-flash")
def get_response(question):
    response = model.generate_content(question)
    return response.text

st.set_page_config(page_title="question and answer")
st.header("Gemini")
input=st.text_input("Input:", key="input")
submit = st.button("ask question")

if submit:
    response = get_response(input)
    st.write(response)