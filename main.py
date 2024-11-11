import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Load the CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS
load_css("styles.css")

# Set up your title
st.markdown("<div class='main'><h1>🤖 AI Chatbot</h1></div>", unsafe_allow_html=True)

# Load API key from environment variable (for secure access)
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API key is missing! Please set the API_KEY in your environment variables.")

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Container for the chat window
chat_container = st.container()

# Input field and button
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input('Type your message...')
    submit_button = st.form_submit_button('Send')

if submit_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"<div class='bubble user-bubble'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bubble ai-bubble'>{message['content']}</div>", unsafe_allow_html=True)
        
        # Display typing animation
        typing_container = st.empty()
        with typing_container:
            st.markdown("<div class='typing-container'><span class='typing'>Typing...</span></div>", unsafe_allow_html=True)
            time.sleep(1)  # Simulate typing delay

        try:
            # Initialize the model
            model = genai.GenerativeModel('gemini-pro')  # Check if this is correct
            chat = model.start_chat(history=[])

            # Send the question to the model and get a response
            response = chat.send_message(user_input)

            # Clear typing animation and display the response
            typing_container.empty()

            if response and response.candidates:
                candidate = response.candidates[0]
                safety_ratings = candidate.safety_ratings
                unsafe = any(
                    rating.probability in ['MEDIUM', 'HIGH'] 
                    for rating in safety_ratings
                )
                if unsafe:
                    st.warning("The content might contain sensitive material and is not displayed.")
                else:
                    response_text = candidate.content.parts[0].text
                    # Add AI response to chat history
                    st.session_state.chat_history.append({'role': 'ai', 'content': response_text})
                    st.markdown(f"<div class='bubble ai-bubble'>{response_text}</div>", unsafe_allow_html=True)
            else:
                st.warning("No valid response received from the model.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
