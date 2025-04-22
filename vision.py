from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import base64
from io import BytesIO

# Load environment variables from .env
load_dotenv()

# Configure the API key for Gemini
genai.configure(api_key=os.getenv("SID_API_KEY"))

# Convert PIL Image to base64 encoded string
def pil_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to load Gemini model and get responses
def get_gemini_response(input_text, image: Image.Image):
    model = genai.GenerativeModel("gemini-1.5-flash")

    image_part = {
        "inline_data": {
            "mime_type": "image/png",
            "data": pil_to_base64(image)
        }
    }

    if input_text.strip() != "":
        parts = [{"text": input_text}, image_part]
    else:
        parts = [image_part]

    response = model.generate_content(parts)
    return response.text

# Streamlit UI
st.set_page_config(page_title="VisionAI")
st.header("🧠 VisionAI - Ask Questions About Your Image")

# Input prompt from the user
input_text = st.text_input("Ask something about the image:", key="input")

# Image upload functionality
uploaded_file = st.file_uploader("Upload an image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Button to ask the model about the image
submit = st.button("Tell me about the image")

# If the "Tell me about the image" button is clicked
if submit:
    if image is not None:
        with st.spinner("Analyzing image..."):
            response = get_gemini_response(input_text, image)

        # Display the response
        st.subheader("The Response is")
        st.markdown(f'<p style="color:blue; font-size: 18px;"><b>You:</b> {input_text}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:green; font-size: 18px;"><b>Bot:</b> {response}</p>', unsafe_allow_html=True)
    else:
        st.warning("Please upload an image before submitting.")
