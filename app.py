
import streamlit as st
import speech_recognition as sr
import time

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Streamlit UI settings
st.set_page_config(page_title="Real-Time Speech-to-Text", layout="wide")

# Custom CSS for black background and white text
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
        color: white;
    }
    .stSelectbox label, .stTextArea label {
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎤 Real-Time Speech-to-Text Conversion")

# Select duration
duration = st.selectbox("Select recording duration (seconds):", [5, 10, 15])

# Function to record audio using the default microphone
def record_audio(duration):
    with sr.Microphone() as source:  # Automatically selects the default microphone
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Increase noise adjustment duration
        st.write("🎤 Speak now!")

        # Capture audio
        audio = recognizer.listen(source, phrase_time_limit=duration)
        st.write("🛑 Recording stopped.")

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "⚠ Could not understand the audio. Speak clearly."
    except sr.RequestError as e:
        return f"⚠ Could not request results from Google Speech Recognition; {e}"
    except Exception as e:
        return f"⚠ An error occurred: {e}"

# UI for recording
if st.button("Start Recording"):
    st.session_state['recognized_text'] = ""
    st.write(f"Recording for {duration} seconds. Please wait...")
    with st.spinner("Processing..."):
        recognized_text = record_audio(duration)
    st.session_state['recognized_text'] = recognized_text

st.text_area("📝 Recognized Text", value=st.session_state.get('recognized_text', ""), height=150)

st.button("🔄 Ready for Next Recording", on_click=lambda: st.session_state.update(recognized_text=""))