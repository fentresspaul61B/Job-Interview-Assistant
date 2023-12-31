"""
An AI dialog model to practice interviews.
"""

# Streamlit used to render web UI.
import streamlit as st

# Audio recorder used to record user audio during dialog.
from audio_recorder_streamlit import audio_recorder

# Base64 used to handle audio byte strings.
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

# Time is used to sleep, so that audio can finish playing, before st 
# does a re run. 
import time

# Audio helper functions used for the dialog.
from st_helpers.audio_helpers import load_eleven_labs_voice
from st_helpers.audio_helpers import autoplay_audio_from_bytes
from st_helpers.audio_helpers import get_audio_duration
from st_helpers.audio_helpers import generate_eleven_labs_audio 
from st_helpers.audio_helpers import set_open_ai_token 
from st_helpers.audio_helpers import get_chat_lang_chain_response 
from st_helpers.audio_helpers import configure_lang_chain
from st_helpers.audio_helpers import generate_chat_response
from st_helpers.audio_helpers import create_context

# Used to edit the default streamlit UI themes. 
from st_helpers.UI_helpers import add_theme

# Open AI used for whisper and chat GPT.
import openai

# Alters default text and background colors.
add_theme(add_gradient=True)

# Used to save user and chatbot dialog.
DIALOG = []

# Creating limit for job description length. 
MAX_CHARS_JOB_DESCRIPT = 1000

# Audio pause threshold, how long of silence before recording stops.
PAUSE_THRESHOLD = 6.0

# Configires open AI settings.
set_open_ai_token()

# Instantiating ElevenLabs voice.
my_voice = load_eleven_labs_voice()


def main():
    """
    Creates UI and runs dialog after password is confirmed.
    """

    # Adding title. 
    st.title("MLE Job Interview Assistant")

    # Enter the password, which I will provide to users. 
    user_input = st.text_input("Enter Password", type="password")

    # Only allow for interview if password is valid.
    if user_input == st.secrets["USER_PW"]:
        
        # Text box for job description. 
        context = st.text_area(
            "Enter Job Description", 
            max_chars=MAX_CHARS_JOB_DESCRIPT
        )
       
        # Generate context for prompt, based on the job description.
        context = create_context(context)
        
        # Instructions for recording audio.
        st.write("Press the button below to record audio.")
        
        # Audio recording button. Have to set key manually, so widgets 
        # do not conflict with eachother. Uses custom st package. May 
        # need maintenence.
        audio_bytes = audio_recorder(
            key="123",
            pause_threshold=PAUSE_THRESHOLD,
            icon_name="square",
            recording_color="#e8b62c",
            neutral_color="#ffae1d",
            text=""
        )
           
        # Check if the session state has the 'processed' attribute.
        if not hasattr(st.session_state, 'processed'):
            st.session_state.processed = False

        # Only process if the 'processed' flag is not set.
        if audio_bytes and not st.session_state.processed:
            
            # Writing audio bytes to the file.
            with open("TTS.wav", mode="wb") as f:
                f.write(audio_bytes)

            # Reading from the file and translating.
            with open("TTS.wav", mode="rb") as f:  
                response = openai.Audio.translate("whisper-1", f)["text"]

            # Saving dialog. 
            DIALOG.append({"user": response})
           
            # Configuring the chat conversation object.
            LANG_CHAIN_CONVERSATION = configure_lang_chain(context)

            # Generating response with context and memory.
            chatbot_response = get_chat_lang_chain_response(
                response,
                lang_chain_conversation=LANG_CHAIN_CONVERSATION
            )
    
            # Saving chat response.
            DIALOG.append({"chat_bot": chatbot_response})

            # Generate TTS with eleven labs.
            audio = generate_eleven_labs_audio(chatbot_response, my_voice)
            
            # Play the audio using custom auto play function, made for 
            # streamlit.   
            autoplay_audio_from_bytes(audio)
           
            # Convert audio bytes into .wav.
            with open('STT.wav', mode='wb') as f:
                f.write(audio)

            # Sleep time is used, so that st does not re run until audio 
            # is finished playing.
            sleep_time = get_audio_duration("STT.wav")

            # Pause to refresh until output audio is completed.
            time.sleep(sleep_time)

            # Set the 'processed' flag.
            st.session_state.processed = True

            # Rerun the app.
            st.experimental_rerun()
    
        # Reset audio_bytes and processed flag for the next interaction.
        audio_bytes = None
        st.session_state.processed = False


if __name__ == "__main__":
    main()


