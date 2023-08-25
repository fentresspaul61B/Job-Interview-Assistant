"""
This is the where the functionality of the dialog is defined. 
"""

# Streamlit used for caching in the UI.
import streamlit as st

# Base 64 used for automatically playing audio in UI.
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

# Json used for extracting and formatting secrets file.
import json

# Pydub mediainfo used for computing the length in seconds of audio. 
from pydub.utils import mediainfo

# Open AI used for text generation. 
import openai

# Lang chain used to create memory for open AI api calls, as well as 
# summarize the conversation so far. 
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI

# OS used to set environment variables. 
import os

CONTEXT_PROMPT = """You are a helpful assistant."""


template = """The following is a friendly conversation between a human and an AI. The AI is not talkative, and gives concise questions and answers. 
In this conversation the AI is role playing as a caring and smart engineering manager who is intervewing a canidate for a machine learning engineering position. 
The AI should ask the canidate questions about their ML projects, ML theory, and applied ML.
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{history}

Conversation:
Human: {input}
AI:"""


def create_context(job_description: str):
    """
    Uses a string of a job description (input from user) to create 
    prompt for dialog and MLE interview.  
    """
    
    template = f"""The following is a friendly conversation between a human and an AI. The AI is not talkative, and gives concise questions and answers. 
In this conversation the AI is role playing as a caring and smart engineering manager who is intervewing a canidate for a machine learning engineering position. 
The AI should ask the canidate questions about their ML projects, ML theory, and applied ML.

Use this job description to guide the interview:

{job_description}

If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{{history}}

Conversation:
Human: {{input}}
AI:"""

    return template


@st.cache_resource
def generate_chat_response(text: str, template=template):

    llm = ChatOpenAI(
        model_name='gpt-4',
        temperature=0,
        max_tokens = 256
    )

    prompt = PromptTemplate(
        input_variables=["history", "input"], template=template
    )

    summary_memory = ConversationSummaryMemory(llm=llm)

    conversation = ConversationChain(
        llm=llm,
        verbose=False,
        memory=summary_memory,
        prompt=prompt
    )

    response = conversation.predict(input=text)

    return response


@st.cache_resource
def configure_lang_chain(template=template):
    """
    Sets up lang chain chat conversation with memory.
    """

    # Choose the LLM to use.
    llm = ChatOpenAI(
        model_name='gpt-4',
        temperature=0,
        max_tokens = 256
    )
    
    # Generate the prompt.
    prompt = PromptTemplate(
        input_variables=["history", "input"], template=template
    )

    # set method of memory.
    summary_memory = ConversationSummaryMemory(llm=llm)

    # Instantiate chat conversation object. 
    conversation = ConversationChain(
        llm=llm,
        verbose=False,
        memory=summary_memory,
        prompt=prompt
    )

    return conversation


def get_chat_lang_chain_response(text, lang_chain_conversation):
    """
    Calls the chat GPT API with context and memory.
    """

    # Generate response from text, with memory.
    response = lang_chain_conversation.predict(input=text)

    return response


@st.cache_data()
def set_open_ai_token():
    """
    Configures open AI token.
    """    
    # Openai used for whisper and GPT.
    
    try:
        OPEN_AI_TOKEN = st.secrets["OPEN_AI_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            OPEN_AI_TOKEN = json.load(f)["OPEN_AI_TOKEN"]

    # Setting the Open AI key.
    openai.api_key = OPEN_AI_TOKEN
    os.environ['OPENAI_API_KEY'] = OPEN_AI_TOKEN


@st.cache_data()
def load_eleven_labs_voice():
    """
    Loads and configures a voice from eleven labs.
    """
    
    # Extracting the eleven labs token.
    
    try:
        ELEVEN_LABS_TOKEN = st.secrets["ELEVEN_LABS_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            ELEVEN_LABS_TOKEN = json.load(f)["ELEVEN_LABS_TOKEN"]
 
    # Configure token.
    set_api_key(ELEVEN_LABS_TOKEN)
    
    # List available voices from eleven labs.
    voices = Voices.from_api()  
    
    # Pick the voice.
    my_voice = voices[-1]
    
    # Settting the consistency in tonality to the voice.
    my_voice.settings.stability = 1.0
    
    # Setting the ammount of similarity to chose voice, higher levels 
    # can create audio artifacts. 
    my_voice.settings.similarity_boost = .5
    
    return my_voice


def generate_eleven_labs_audio(text: str, voice: str) -> bytes:
    """
    Generates realistic speech from eleven labs API, and returns audio 
    bytes.
    """

    # Creates audio bytes of realistic sounding voice.
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_monolingual_v1"
    )

    return audio


def autoplay_audio_from_bytes(audio_data: bytes):
    """
    Autoplays audio from a byte string.
    """
    
    # Convert audio bytes into base 64 string.
    b64 = base64.b64encode(audio_data).decode()

    # CSS to enable streamlit to auto play.
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """
    
    # Enabling the custom CSS for streamlit.
    st.markdown(
        md,
        unsafe_allow_html=True,
    )

    # st.experimental_rerun()


def get_audio_duration(filename: str) -> float:
    """
    Get the duration of an audio file in seconds.
    """
    
    # Extract audio meta data.
    info = mediainfo(filename)

    duration = float(info['duration'])

    return duration


