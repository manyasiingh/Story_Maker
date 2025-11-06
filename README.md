Personalized AI Story Maker

✨ Project Overview (GenAI LLM)

This is a dynamic web application built with Streamlit and the Google Gemini API that generates unique, personalized short stories based on user-defined inputs (character name, personality, hobby, setting, and theme). The application leverages the power of the Gemini LLM to provide real-time text streaming for an engaging user experience.

🛠️ Technology Stack

Component

Technology

Description

Generative AI

Google Gemini API (gemini-2.5-flash)

The core LLM for story generation.

Frontend/App

Streamlit

Python framework used for rapid web application deployment.

Language

Python 3.8+

Primary language for application logic and scripting.

Secrets

python-dotenv

Used for secure management of API keys in local development.

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

This application is optimized for deployment on Streamlit Cloud.

For deployment, you must configure your secret key directly in the Streamlit Cloud dashboard or use a secrets.toml file within a .streamlit folder:

# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"


Key Technical Features

API Streaming: Utilizes generate_content_stream for efficient, chunk-by-chunk story output.

Robustness: Includes dynamic fallback logic to ensure compatibility with various versions of the Gemini SDK during deployment.

Secure Secrets: Uses environment variables/Streamlit secrets to keep the API key out of the source code.
