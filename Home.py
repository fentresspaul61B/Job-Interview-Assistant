"""
Landing page shows a description of the app, and explains how to use it.
"""

import streamlit as st 

from st_helpers.UI_helpers import add_theme, apply_home_page_gradient

from streamlit_extras.switch_page_button import switch_page


add_theme(add_gradient=True)

apply_home_page_gradient()

st.title("Welcome. 🐠")

start_interview = st.button("Start the Interview!")

if start_interview:
    switch_page("Interview")

# add_theme(add_gradient=True)

