import streamlit as st 

from st_helpers.UI_helpers import add_theme


# Alters default text and background colors.
add_theme(add_gradient=True)

# 
st.title("MLE Interview Assistant")

#
st.header("How It Works")

st.write(
"""Single shot prompt engineering was applied, along with summarized memory in order to guide the LLM to role play as an interviewer, and ask relevant questions in a back and forth dialog format. 

A. User Speaks into APP
B. Whisper translates speech to text.
C. Text from user is turned into a prompt using LangChain. and response is generated using GPT-4. 
D. Response is converted from text to speech using ElevenLabs."""
)
#
st.image("images/MLE_interview_diagram.png")
