from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def set_bg_hack_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("https://pxwall.com/wp-content/uploads/2018/06/Wallpaper%20lime,%20green,%204k,%20Food%20391081808.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-blur: 40px;
        }}
        .stButton>button {{
            background-color: #0c6317;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 20px;
        }}
        .stButton>button:hover {{
            background-color: #228B22;
            color:white;
            border-color:white;
        }}
        .stWrite {{
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if not image:
        st.warning("Please provide the image of the food", icon="⚠️")
        return None
    else:
        response = model.generate_content(['''You are an expert in nutrition where you need to see the food items from the image
               and calculate the total calories, allergens, and health benefits. Also, provide the details of every food item with calorie intake''', image])
    return response.text if response else "No response received."

st.set_page_config(page_title="HealthyFoods", page_icon="🥑")
set_bg_hack_url()

st.header("HealthyFoods")

uploaded_file = st.file_uploader("Choose an image of your food....", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Get Information for the food")

if submit:
    response = get_gemini_response(image)
    if response:
        st.markdown(f"""
        <div class="stWrite">
            <h3>Food Information:</h3>
            <p>{response}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No information could be retrieved.")
