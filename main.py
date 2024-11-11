import streamlit as st
import google.generativeai as genai
import os

# Custom CSS for UI with plain colors and subtle styles
css = """
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* General body styling */
/* General body styling */
body {
    background-color: #f1f8ff;  /* Soft light blue for a calm look */
    color: #444444;  /* Slightly lighter dark text for better readability */
    font-family: 'Roboto', sans-serif;  /* Clean, modern sans-serif font */
}

/* Main container styling */
.main {
    background-color: #ffffff;  /* White background for clarity */
    color: #444444;  /* Matching text color for consistency */
    font-family: 'Roboto', sans-serif;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);  /* Soft shadow for depth */
}

/* Header styling */
h1 {
    color: #2C3E50;  /* Darker blue color for professionalism */
    font-size: 36px;
    text-align: center;
    margin-bottom: 20px;
    font-family: 'Montserrat', sans-serif;  /* Modern, bold font for headings */
}

/* Input box styling */
.stTextInput input {
    background-color: #ffffff;  /* White background for the input box */
    color: #333333;  /* Dark text for visibility */
    border-radius: 5px;
    padding: 12px 20px;
    border: 2px solid #3498db;  /* Soft blue border */
    font-family: 'Roboto', sans-serif;
    font-size: 16px;
}

/* Button styling */
.stButton button {
    background-color: #3498db;  /* Blue background for buttons */
    color: white;
    border-radius: 5px;
    padding: 12px 20px;
    font-size: 16px;
    font-family: 'Roboto', sans-serif;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}

.stButton button:hover {
    background-color: #2980b9;  /* Slightly darker blue on hover */
}

.stButton button:active {
    transform: translateY(2px);  /* Button press effect */
}

/* Typing container styling */
.typing-container {
    background-color: #f9f9f9;  /* Soft gray background for the response area */
    padding: 12px;
    border-radius: 5px;
    border: 1px solid #3498db;  /* Blue border around the typing box */
    color: #444444;
    font-family: 'Roboto', sans-serif;
}

/* Typing effect styling */
.typing {
    font-family: 'Roboto', sans-serif;
    font-size: 18px;
    line-height: 1.6;
    color: #333333;  /* Dark text for easy reading */
    white-space: pre-wrap;
}

/* Warning and error message styling */
.stWarning {
    color: #e67e22;  /* Warm orange for warnings */
    font-size: 18px;
    font-weight: bold;
    font-family: 'Roboto', sans-serif;
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
            except Exception as e:  # Catch any general exception
                st.error(f"An error occurred: {e}")