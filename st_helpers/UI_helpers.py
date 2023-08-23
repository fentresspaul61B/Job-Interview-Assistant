"""
This file contains helper functions for visual and functional purposes.
"""

import streamlit as st 
from PIL import Image

LIGHT_GRADIENT = """
"background: linear-gradient(
    299deg, 
    rgba(250,244,255,1) 0%, 
    rgba(244,255,237,1) 45%, 
    rgba(244,253,255,1) 100%
);
"""

BRIGHT_GRADIENT = """
background: linear-gradient(
    90deg, 
    rgba(244,232,255,1) 0%, 
    rgba(230,255,214,1) 45%, 
    rgba(210,248,255,1) 100%
);
"""

FLAT_GRADIEN = """
background: linear-gradient(
    299deg, 
    rgba(222,209,233,1) 0%, 
    rgba(226,239,218,1) 45%, 
    rgba(218,233,235,1) 100%
);
"""

TEST_GRADIENT = """
background: linear-gradient(
    85deg, 
    rgba(255,238,199,1) 0%, 
    rgba(227,255,223,1) 33%,
    rgba(252,244,255,1) 66%,
    rgba(227,247,255,1) 100%
);
""" 

PRODUCTION_FONT_URL = "https://fonts.googleapis.com"

PRODUCTION_GOOGLE_FONT = "css2?family=Roboto:wght@100&display=swap" 


def apply_font_to_st_page(
        font_url: str = PRODUCTION_FONT_URL,
        font:     str = PRODUCTION_GOOGLE_FONT
    ):
    """
    This function uses css and streamlit markdown to alter the font of 
    the page. I am using a google font, so that the font matches the 
    font in the google form.

    Inputs:
        font_url: str = The google url to the font.
        font: str = The remaining css code to execute the google url.
    """

    streamlit_style = f"""
	<style>
     @import url('{font_url}/{font}');
       
	html, body [class*="css"]  {{
	    font-family: 'Roboto', 
        sans-serif;
	}}
	</style>
    """

    st.markdown(streamlit_style, unsafe_allow_html=True)
  

def apply_gradient_to_st_page(
        gradient: str,
        font_url: str = PRODUCTION_FONT_URL,
        font:     str = PRODUCTION_GOOGLE_FONT
    ):
    """
    This function uses css and streamlit markdown to apply a morphing 
    gradient to the background of the page. The google font has to be 
    re-applied otherwise this layer will contain the default font.

    There are warning about using HTML elements that may change, so this
    is something I need to watch out for during deployment, and in prod.

    Inputs:
        gradient: str = any number of RGB colors, and their percents to  
        be applied.
        font_url: str = The google url to the font.
        font: str = The remaining css code to execute the google url.
    """
 
    streamlit_style = f"""
         <style>
        @import url('{font_url}/{font}');
       
        @keyframes gradientBackground {{
            0% {{
                background-position: 100% 0%;
            }}
            25% {{
                background-position: 50% 50%;
            }}
            50% {{
                background-position: 0% 100%;
            }}
            75% {{
                background-position: 50% 50%;
            }}
            100% {{
                background-position: 100% 0%;
            }}
        }}

        html, body [class*="main css-uf99v8 ea3mdgi5", class*="element-container css-1ims0h4 e1f1d6gn2"] {{
            font-family: 'Roboto', sans-serif !important;
            {gradient}
            background-size: 200% 200%;
            animation: gradientBackground 15s infinite;
        }}
        </style>
    """

    st.markdown(streamlit_style, unsafe_allow_html=True)


def add_theme():
    """
    This function applies a consistent theme for each page in the front end.
    There are 3 steps for adding the theme. 
    1. Change the font of all objects in the front end. 
    2. Apply the gradient color to specific sections of the front end.
    3. Add the side bar, with the logo gif.
    """
    
    # 1. Change font.
    apply_font_to_st_page()

    # 2. Dynamic gradient background.
    apply_gradient_to_st_page(TEST_GRADIENT)
    
