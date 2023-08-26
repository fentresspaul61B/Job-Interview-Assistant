"""
Landing page shows a description of the app, and explains how to use it.
"""

import streamlit as st 

from st_helpers.UI_helpers import add_theme, apply_home_page_gradient

from streamlit_extras.switch_page_button import switch_page


add_theme(add_gradient=True)

# apply_home_page_gradient()

st.title("MLE Interview Assistant")

st.header("Helping engineers practice realistic and targeted Machine Learning interviews.")

st.subheader("Welcome!")


st.write(
"""Welcome to your personal Machine Learning Engineering (MLE) interview simulation. This project utilizes generative AI to simulate realistic MLE interviews, based on the job descriptions you provide."""
)

start_interview = st.button("Start the Interview!")

if start_interview:
    switch_page("Interview")

# add_theme(add_gradient=True)

