import streamlit as st
import google.generativeai as genai

# Load the CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS file
load_css("styles.css")

# Set up your title
st.title("🤖 AI Question Answering App")

# Hardcode the API key directly (not secure)
api_key = "AIzaSyDo2yPvvj9rVhWmQUQPGzIuMb_JAqPhyME"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Input from the user
text = st.text_input('Enter Your Question')

# Check if the user has entered a question
if text:
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        # Send the question to the model and get a response
        response = chat.send_message(text)

        # Check safety ratings
        if response and response.candidates:
            candidate = response.candidates[0]
            safety_ratings = candidate.safety_ratings
            # Check safety ratings
            unsafe = any(
                rating.probability in ['MEDIUM', 'HIGH'] 
                for rating in safety_ratings
            )
            if unsafe:
                st.warning("The content might contain sensitive material and is not displayed.")
            else:
                response_text = candidate.content.parts[0].text
                st.write(response_text)  # Display the full response text directly
        else:
            st.warning("No valid response received from the model.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
