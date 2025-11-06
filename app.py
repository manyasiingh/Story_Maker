import streamlit as st
import openai
import os
from dotenv import load_dotenv

# --- Configuration & Setup ---

# Load environment variables (like API key) from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the OpenAI client using the loaded API key
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    st.error("OpenAI API Key not found! Please create a '.env' file or set the environment variable.")
    client = None

# --- Story Generation Function ---

def generate_story(hero_name, theme, length, genre, client):
    """
    Generates a personalized story using the OpenAI Chat API.
    """
    # Create a detailed system and user prompt for the LLM
    system_prompt = (
        "You are a master storyteller specializing in personalized tales. "
        "Your task is to write a compelling, creative, and engaging story. "
        "The story should be well-structured with a clear beginning, middle, and end."
    )
    
    user_prompt = f"""
    Write a {length} story for a child.
    
    The main character's name is **{hero_name}**.
    The story's primary theme is: **{theme}**.
    The story's genre/style should be: **{genre}**.
    
    Make sure the story is positive, imaginative, and appropriate for all ages.
    Do not include the user prompt or any introductory text. Just start the story.
    """
    
    if not client:
        return "Error: Cannot connect to AI service. Check your API key."

    try:
        with st.spinner("🌌 Weaving a magnificent story... Please wait."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # A fast and capable model for this task
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7, # Higher temperature for more creativity
                max_tokens=1500 # Set a max token limit for story length
            )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"An API Error occurred: {e}"

# --- Streamlit App Layout ---

st.set_page_config(page_title="Personalized Story Generator", layout="wide")

st.title("📖 Personalized Story Generator 📖")
st.markdown("Enter details to create a unique adventure tailored just for you!")

# Create a sidebar for user inputs
with st.sidebar:
    st.header("Story Ingredients 📝")
    hero_name = st.text_input("Main Character's Name (e.g., Mia or Sparky)", "A brave adventurer")
    theme = st.text_input("Story Theme (e.g., Discovering a lost city)", "Learning how to share")
    
    # Select boxes for structured input
    length = st.select_slider(
        "Story Length",
        options=['Very Short (1-2 min)', 'Short (3-5 min)', 'Medium (5-8 min)'],
        value='Short (3-5 min)'
    )
    
    genre = st.selectbox(
        "Genre",
        options=['Fantasy', 'Sci-Fi', 'Mystery', 'Fairytale', 'Funny'],
        index=0
    )
    
    generate_button = st.button("Generate Story!", type="primary")

st.divider()

# Main content area for the generated story
if generate_button:
    if not hero_name or not theme:
        st.warning("Please enter a name and a theme to begin.")
    else:
        # Call the generation function
        story_content = generate_story(
            hero_name=hero_name,
            theme=theme,
            length=length.split('(')[0].strip(), # Pass only the descriptive part
            genre=genre,
            client=client
        )
        
        # Display the results
        st.header(f"The Story of {hero_name} ({genre})")
        st.markdown(story_content)
        
        # Add a download button
        st.download_button(
            label="Download Story as .txt",
            data=story_content,
            file_name=f"{hero_name}_{genre}_Story.txt",
            mime="text/plain"
        )
else:
    st.info("💡 Fill out the details in the sidebar and click 'Generate Story!' to begin your adventure.")

st.markdown(
    """
    ---
    *Built with Streamlit and the OpenAI API.*
    """
)