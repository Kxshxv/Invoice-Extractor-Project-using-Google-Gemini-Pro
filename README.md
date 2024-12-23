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
Note:
 * This is a basic example and can be further extended to support different invoice formats and extract more specific data based on user requirements.
I hope this README.md file provides a clear overview of your project. Let me know if you have any other questions.
