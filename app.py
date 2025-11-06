import os
import streamlit as st
import io
from google import genai
from google.genai.errors import APIError
from PIL import Image
from dotenv import load_dotenv

# --- 1. CONFIGURATION AND CLIENT INITIALIZATION ---

# Load environment variables (must happen before Streamlit runs the main logic)
# This will load GEMINI_API_KEY from the .env file if available locally
load_dotenv()

# Check if the API key is available
API_KEY = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def load_gemini_client(key):
    """Initializes and caches the Gemini client."""
    if not key:
        # In a real deployed environment (like Streamlit Cloud), API_KEY would be set
        # as a secret, and this path would likely not be hit.
        return None 
    try:
        # The client constructor can take the API key directly
        client = genai.Client(api_key=key)
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None

# --- 2. GENERATION FUNCTION ---

def generate_content_stream(client: genai.Client, prompt: str, uploaded_file):
    """
    Generates content based on text and an optional image, streaming the output.
    """
    contents = []
    
    # Handle image content if uploaded
    if uploaded_file is not None:
        try:
            # Read image data from the UploadedFile object using BytesIO
            image_data = uploaded_file.read()
            img = Image.open(io.BytesIO(image_data))
            st.image(img, caption="Uploaded Image", use_column_width=True)
            contents.append(img)
        except Exception as e:
            st.error(f"Could not load image: {e}")
            return
            
    # Add text prompt last
    contents.append(prompt)
    
    st.subheader("Model Response")
    
    try:
        # Use generate_content_stream for a better user experience
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=contents
        )
        
        # Use st.write_stream to display the response in real-time
        st.write_stream(response_stream)
        
    except APIError as e:
        st.error(f"An API error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# --- 3. STREAMLIT APP LAYOUT ---

def main():
    st.set_page_config(page_title="Gemini Streamlit Multimodal Demo", layout="centered")
    
    st.title("🤖 Gemini API Streamlit App")
    st.markdown("Use this app to generate text or analyze an image using the `gemini-2.5-flash` model.")
    
    # 3a. API Key Check and Client Loading
    if not API_KEY:
        st.error(
            "API Key not found! Please set your `GEMINI_API_KEY` in the `.env` file (for local use) or as a Streamlit Cloud secret."
        )
        return

    client = load_gemini_client(API_KEY)
    if client is None:
        return # Client failed to initialize

    # 3b. User Inputs
    
    uploaded_file = st.file_uploader(
        "Upload an Image (Optional)", 
        type=["jpg", "jpeg", "png", "webp"],
        key="image_uploader"
    )
    
    prompt = st.text_area(
        "Enter your prompt or question:",
        "What is a list and a tuple in Python, and how does the object in the image relate to either of those concepts?",
        height=150
    )
    
    # 3c. Generation Trigger
    if st.button("Generate Response", use_container_width=True, type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt before generating content.")
        else:
            # Show a spinner while processing
            with st.spinner("Generating content..."):
                generate_content_stream(client, prompt, uploaded_file)
                
    st.markdown("---")
    st.caption("Powered by Google Gemini API and Streamlit. Check the console for full details.")

if __name__ == "__main__":
    main()