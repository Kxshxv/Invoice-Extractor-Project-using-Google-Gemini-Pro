# Invoice-Extractor-Project-using-Google-Gemini-Pro

This project allows users to upload images of invoices and extract data using prompts or a predefined command to get a JSON response. The extracted data is then stored in a MySQL database.

Features
 * Upload invoice images
 * Provide prompts to extract specific data from invoices
 * Extract all text data in JSON format using a predefined prompt
 * Store extracted data in a MySQL database

Requirements
 * Python 3.x
 * Streamlit (pip install streamlit)
 * Google GenerativeAI library (pip install google-generativeai)
 * Pillow (pip install Pillow)
 * mysql-connector-python (pip install mysql-connector-python)

Installation
 * Clone this repository or download the files.
 * Install the required libraries:

pip install streamlit google-generativeai
Pillow mysql-connector-python

 * Configure your Google GenerativeAI API key by creating a .env file in the project root directory and adding the following line:
GOOGLE_API_KEY=<YOUR_API_KEY>

 * Replace the placeholder values in the connect_to_db function (connect.py) with your MySQL database connection details:
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",      # Replace with your database host
        user="root",           # Replace with your database username
        password="keshav",   # Replace with your database password
        database="demo"        # Replace with your database name)

Usage
 * Run the application using:
streamlit run app.py

 * Access the application in your web browser at http://localhost:8501.
 * Upload an invoice image and provide a prompt to extract specific data.
 * Alternatively, use the predefined prompt "extract all the text data in json format" to get a JSON response containing all extracted text data.
Database
The extracted data is stored in a MySQL database table named InvoiceResponses. The table schema includes the following columns:
 * id (INT, primary key): Auto-incrementing ID
 * input_prompt (VARCHAR): The prompt provided by the user
 * input_text (VARCHAR): Any additional text input provided by the user
 * response (TEXT): The extracted data from the invoice
 
walkthrough of the code:

1. Import necessary libraries:

from dotenv import load_dotenv
import streamlit as st  
import os
from PIL import Image
import google.generativeai as genai
import mysql.connector
from datetime import datetime

 * dotenv: Used to load environment variables from a .env file (recommended for sensitive information like API keys).
 * streamlit: The core library for building interactive web applications.
 * os: Provides functions for interacting with the operating system (e.g., accessing environment variables).
 * PIL: The Python Imaging Library, used for image manipulation.
 * google.generativeai: The library for interacting with Google Generative AI models.
 * mysql.connector: The library for connecting to MySQL databases.
 * datetime: Provides classes for working with dates and times.

2. Load environment variables:
load_dotenv()

Loads environment variables from the .env file, allowing you to securely store sensitive information like your Google API key.
3. Configure Generative AI:
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

 * Configures the Google Generative AI library with your API key.
 * Specifies the Gemini 1.5 Flash model for generating responses.

4. MySQL Database Connection:
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",      # Replace with your database host
        user="root",           # Replace with your database username
        password="keshav",   # Replace with your database password
        database="demo "   # Replace with your database name
    )

 * Defines a function to establish a connection to the MySQL database.
 * Important: Replace the placeholder values with your actual database credentials.

5. Insert data into the database:
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

 * Defines a function to insert the generated response into the InvoiceResponses table in the database.
 * Uses parameterized queries to prevent SQL injection vulnerabilities.

6. Helper function to process image details:
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

 * This function prepares the uploaded image data in the format required by the google.generativeai library.

7. Helper function to get Gemini response:
def get_gemini_response(input_prompt, image, input_text):
    response = model.generate_content([input_prompt, image[0], input_text])
    return response.text

 * This function calls the Gemini model to generate a response based on the provided input prompt, image data, and any additional text input.

8. Streamlit configuration:
st.set_page_config(page_title="Multi-Language Invoice Extractor")

 * Sets the page title of the Streamlit application.

9. Input fields:
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

 * Creates input fields for the user to provide an input prompt and upload an image.
 * Displays the uploaded image using st.image().

10. Submit button:
submit = st.button("Tell me about the invoice")

 * Creates a submit button for the user to trigger the data extraction process.

11. Input prompt for the model:
input_prompt = """You are an expert in understanding invoices. We will upload an image of an invoice, and you will tell us about the invoice."""

 * Defines the base input prompt for the Gemini model.

12. Process submission:
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

 * This block handles the submission event:
   * Checks if the user has provided both an input prompt and an image.
   * Calls the get_gemini_response() function to obtain the extracted data.
   * Displays the extracted data to the user.
   * Inserts the extracted data into the database using the insert_response_to_db() function.
   * Displays success or error messages to the user.

I hope this walkthrough provides a comprehensive understanding of the code and its functionality. 
 Note:
 * This is a basic example and can be further extended to support different invoice formats and extract more specific data based on user requirements.
I hope this README.md file provides a clear overview of your project. Let me know if you have any other questions.
