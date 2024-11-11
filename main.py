import streamlit as st
import google.generativeai as genai
import os

# Custom CSS for UI with plain colors and subtle styles
css = """
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* General body styling */
    body {
        background-color: #f4f7fc;  /* Lighter background for clean look */
        color: #333333;  /* Darker text for better readability */
        font-family: 'Orbitron', sans-serif;
    }

    /* Main container styling */
    .main {
        background-color: #ffffff;  /* White background for the content area */
        color: #333333;  /* Dark text color for contrast */
        font-family: 'Orbitron', sans-serif;
        padding: 20px;
        border-radius: 10px;
        box-shadow: none;  /* Removed the glow effect */
    }

    /* Header styling */
    h1 {
        color: #4CAF50;  /* Subtle green color */
        font-size: 36px;
        text-align: center;
        margin-bottom: 20px;
    }

    .stMarkdown h1 {
        font-family: 'Orbitron', sans-serif;
    }

    /* Input box styling */
    .stTextInput input {
        background-color: #ffffff;  /* White background for the input box */
        color: #333333;  /* Dark text for visibility */
        border-radius: 5px;
        padding: 12px 20px;
        border: 2px solid #4CAF50;  /* Green border for a clean look */
    }

    /* Button styling */
    .stButton button {
        background-color: #4CAF50;  /* Green background */
        color: white;
        border-radius: 5px;
        padding: 12px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }

    .stButton button:hover {
        background-color: #45a049;  /* Darker green on hover */
    }

    .stButton button:active {
        transform: translateY(2px);  /* Press effect */
    }

    /* Typing container styling */
    .typing-container {
        background-color: #f4f7fc;  /* Light background for the typing box */
        padding: 12px;
        border-radius: 5px;
        border: 1px solid #4CAF50;  /* Green border around the response area */
        color: #333333;
    }

    /* Typing effect styling */
    .typing {
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        line-height: 1.5;
        white-space: pre-wrap;
    }

    /* Warning and error message styling */
    .stWarning {
        color: #FF9800;
        font-size: 18px;
        font-weight: bold;
    }
"""

# Inject custom CSS into the app
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Set up your title
st.title("🤖 AI Question Answering App")

# Load API key securely from environment variable
api_key = os.getenv("API_KEY")  # Load API key from environment variable

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key is missing or not set correctly.")

# Add a container for the main content
with st.container():
    # Input from the user
    text = st.text_input('Enter Your Question')

    # Add a button to submit the question for better user control
    if st.button('Get Answer'):
        # Check if the user has entered a question
        if text:
            try:
                # Initialize the model
                model = genai.GenerativeModel('gemini-pro')  # Ensure the model name is correct
                chat = model.start_chat(history=[])

                # Send the question to the model and get a response
                response = chat.send_message(text)

                # Check if the response contains candidates
                if response and response.candidates:
                    candidate = response.candidates[0]
                    safety_ratings = candidate.safety_ratings

                    # Check safety ratings for potentially sensitive content
                    unsafe = any(rating.probability in ['MEDIUM', 'HIGH'] for rating in safety_ratings)

                    if unsafe:
                        st.warning("The content might contain sensitive material and is not displayed.", icon="⚠️")
                    else:
                        response_text = candidate.content.parts[0].text
                        st.markdown(f'<div class="typing-container"><div class="typing">{response_text}</div></div>', unsafe_allow_html=True)  # Add typing effect for response
                else:
                    st.warning("No valid response received from the model.", icon="⚠️")
            except genai.errors.ApiError as api_err:
                st.error(f"API error occurred: {api_err}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
