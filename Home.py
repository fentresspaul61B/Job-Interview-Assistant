"""
Landing page shows a description of the app, and explains how to use it.
"""

import streamlit as st 

from st_helpers.UI_helpers import add_theme

from streamlit_extras.switch_page_button import switch_page


add_theme(add_gradient=True)

st.title("Welcome. 🐠")

start_interview = st.button("Start the Interview!")

if start_interview:
    switch_page("Interview")

# add_theme(add_gradient=True)

