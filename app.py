from dotenv import load_dotenv
import streamlit as st  
import os
from PIL import Image
import google.generativeai as genai
import mysql.connector
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# MySQL Database Connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",      # Replace with your database host
        user="root",           # Replace with your database username
        password="keshav",   # Replace with your database password
        database="demo "   # Replace with your database name
    )

# Insert data into the database
def insert_response_to_db(input_prompt, input_text, response):
    try:
        db = connect_to_db()
        cursor = db.cursor()
        query = """
        INSERT INTO InvoiceResponses (input_prompt, input_text, response)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (input_prompt, input_text, response))
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        st.error(f"Failed to insert into database: {e}")

# Helper function to process image details
def input_image_details(uploaded_file):   
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

# Helper function to get Gemini response
def get_gemini_response(input_prompt, image, input_text):
    response = model.generate_content([input_prompt, image[0], input_text])
    return response.text

# Streamlit configuration
st.set_page_config(page_title="Multi-Language Invoice Extractor")

# Input fields
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

# Submit button
submit = st.button("Tell me about the invoice")

# Input prompt for the model
input_prompt = """You are an expert in understanding invoices. We will upload an image of an invoice, and you will tell us about the invoice."""

# Process submission
if submit:
    try:
        if not input_text:
            st.error("Please enter an input prompt.")
        elif not uploaded_file:
            st.error("Please upload an image.")
        else:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input_text)
            st.subheader("The response is:")
            st.write(response)
            
            # Insert response into the database
            insert_response_to_db(input_prompt, input_text, response)
            st.success("Response has been saved to the database.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
