"""
Streamlit Cheat Sheet

App to summarise streamlit docs v1.25.0

There is also an accompanying png and pdf version

https://github.com/daniellewisDL/streamlit-cheat-sheet

v1.25.0
20 August 2023

Author:
    @daniellewisDL : https://github.com/daniellewisDL

Contributors:
    @arnaudmiribel : https://github.com/arnaudmiribel
    @akrolsmir : https://github.com/akrolsmir
    @nathancarter : https://github.com/nathancarter

"""

import streamlit as st
from pathlib import Path
import base64

# Initial page config

st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    cs_sidebar()
    cs_body()
    return None

# Thanks to streamlitopedia for the following code snippet

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# sidebar

def cs_sidebar():

    st.sidebar.slider("Select sample size: ", min_value=1, max_value=100, value=1)
    while True:
        seed_input = st.sidebar.text_area("Enter Seed: ", "")
        try:
            int(seed_input)
        except:
            st.sidebar.text("Error: Only accept integers")
        if len(str(seed_input)) == 10:
            break
        else:
            st.sidebar.text("Seed must be 10 digits")
    st.sidebar.text("Success!")
    return None

##########################
# Main body of cheat sheet
##########################
def create_bar_chart(data):
    st.bar_chart(data)
    return None



def display_text_in_textbox(text):       #takes texr as parameter - for the GPT bs
    st.text_area("Text Box", text)
    return None

def display_image_from_sdiffusion(url):
    st.image(url, caption='Your Image Caption', use_column_width=True)
    return None


def generate(): #function to generate 
    st.write("Button clicked! My custom function executed.")



def cs_body():
    text_message = "Hello, this is a text message." # example data
    data = {
    'Variable1': [1, 2, 3, 4, 5],
    'Variable2': [10, 15, 8, 12, 7] #example data
    }
    display_text_in_textbox(text_message)
    # Create a button
    button_clicked = st.button("Generate a retard")

# Check if the button is clicked
    if button_clicked:
        generate()
    st.bar_chart(data)
    display_image_from_sdiffusion("https://example.com/your_image.jpg")

    
    return None

# Run main()

if __name__ == '__main__':
    main()
