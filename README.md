Personalized AI Story Maker

✨ Project Overview

This is a dynamic web application built with Streamlit and the Google Gemini API that generates unique, personalized short stories based on user-defined inputs (character name, personality, hobby, setting, and theme). The application features real-time text streaming for an engaging user experience.

🛠️ Technology Stack

Language: Python

Web Framework: Streamlit

AI Backend: Google Gemini API (google-genai SDK)

Dependency Management: requirements.txt

Environment Management: python-dotenv

🚀 Getting Started Locally

Prerequisites

Python 3.8+

A Google Gemini API Key.

1. Clone the repository

git clone <YOUR_REPO_URL>
cd personalized-story-maker


2. Set up the Environment

Create a file named .env in the root directory and add your API key:

GEMINI_API_KEY="YOUR_API_KEY_HERE"


3. Install Dependencies

Install all required Python packages:

pip install -r requirements.txt


4. Run the Application

Start the Streamlit application:

streamlit run app.py


The application will open automatically in your default web browser.

☁️ Deployment

This application is designed to be easily deployed on Streamlit Cloud.

For deployment, replace the local .env file with a Streamlit-compatible secrets.toml file in a .streamlit folder and add your key:

# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"


Key Technical Features

API Streaming: Utilizes the generate_content_stream method for chunk-by-chunk story output.

Robustness: Includes dynamic fallback logic to ensure compatibility with various versions of the Gemini SDK during deployment.

Secure Secrets: Uses environment variables/Streamlit secrets to keep the API key out of the source code.
