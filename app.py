import os
import streamlit as st
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

# --- 1. CONFIGURATION AND CLIENT INITIALIZATION ---

# Load environment variables from the .env file (if running locally)
load_dotenv()

# The client will automatically pick up the key from the environment
API_KEY = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def load_gemini_client(key):
    """Initializes and caches the Gemini client."""
    if not key:
        return None 
    try:
        # Initializing client with the key
        client = genai.Client(api_key=key)
        return client
    except Exception as e:
        # In a real deployed environment, st.secrets is used, but for local use we check .env
        st.error(f"Error initializing Gemini client. Check your GEMINI_API_KEY in .env or secrets: {e}")
        return None

# --- 2. GENERATION FUNCTION ---

def generate_story_stream(client: genai.Client, user_details: dict):
    """
    Constructs the prompt and streams the generated story.
    Includes fallback logic for older SDKs that don't support system_instruction.
    """
    # Define the System Instruction
    system_instruction_text = (
        "You are a magical storyteller. You must write a creative, engaging, and unique short story "
        "based ONLY on the user's provided details. Structure the story with an introduction, conflict, and resolution. "
        "The story should have a clear beginning and end."
    )

    # Detailed prompt construction based on user inputs
    prompt = f"""
    Please write a personalized story for the main character named '{user_details['name']}'.
    
    Story Theme/Genre: {user_details['theme']}
    Key Setting/Location: {user_details['setting']}
    Length: {user_details['length']} words.

    The main character, {user_details['name']}, loves {user_details['hobby']} and their defining personality trait is {user_details['trait']}.
    Begin the story now:
    """
    
    st.subheader(f"📖 The Story of {user_details['name']}")
    
    try:
        # --- ATTEMPT 1: Modern SDK (using system_instruction keyword) ---
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
            system_instruction=system_instruction_text
        )
        
        # Streamlit's built-in stream writer displays the content as it arrives
        st.write_stream(response_stream)
        
    except TypeError as e:
        # --- FALLBACK: If 'system_instruction' keyword fails, use the old SDK method ---
        if "'system_instruction'" in str(e):
            st.warning("⚠️ Using legacy SDK method. Please ensure 'google-genai' is updated.")
            
            # Combine system instruction and user prompt into a single contents string
            fallback_prompt = f"{system_instruction_text}\n\nUSER PROMPT:\n{prompt}"
            
            # Call without system_instruction argument
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=fallback_prompt
            )
            st.write_stream(response_stream)
        else:
            # Re-raise other TypeError exceptions
            raise e
            
    except APIError as e:
        st.error(f"An API error occurred during story generation: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# --- 3. STREAMLIT APP LAYOUT ---

def main():
    st.set_page_config(page_title="Personalized Story Maker", layout="wide")
    
    st.title("✨ Personalized Story Maker")
    st.markdown("Enter details about your character and world, and let the Gemini API weave a unique tale!")
    
    # 3a. API Key Check and Client Loading
    if not API_KEY:
        st.error(
            "API Key not found! Please set your `GEMINI_API_KEY` in the `.env` file (for local use) or as a Streamlit Cloud secret."
        )
        return

    client = load_gemini_client(API_KEY)
    if client is None:
        return

    # 3b. User Inputs (Sidebar for cleaner main area)
    with st.sidebar:
        st.header("Character & Story Details")
        
        # Input fields for personalization
        name = st.text_input("Main Character's Name:", "Elara")
        trait = st.text_input("Main Personality Trait (e.g., Curious, Brave):", "Determined")
        hobby = st.text_input("A favorite hobby/interest:", "Stargazing")
        
        st.subheader("World Details")
        setting = st.selectbox(
            "Key Setting/Location:",
            ["A bustling futuristic city", "An ancient, misty forest", "A remote, ice-covered planet", "A magical library"]
        )
        theme = st.selectbox(
            "Story Theme/Genre:",
            ["Fantasy Adventure", "Sci-Fi Mystery", "Historical Romance", "Modern Comedy"]
        )
        length = st.select_slider(
            "Story Length (approximate words):",
            options=[200, 350, 500, 750],
            value=350
        )
        
        # Dictionary to pass all details to the generation function
        user_details = {
            'name': name,
            'trait': trait,
            'hobby': hobby,
            'setting': setting,
            'theme': theme,
            'length': length
        }

    # 3c. Generation Trigger (in the main area)
    st.write("---")

    if st.button("Generate My Personalized Story!", use_container_width=True, type="primary"):
        if not name.strip():
            st.warning("Please enter a name for your main character.")
        else:
            # Clear previous outputs (optional, but nice for clean reruns)
            st.empty() 
            
            # Show a spinner while processing
            with st.spinner(f"Weaving a {theme} tale about {name}..."):
                generate_story_stream(client, user_details)
                
    st.markdown("---")
    st.caption("Powered by Google Gemini API and Streamlit.")

if __name__ == "__main__":
    main()