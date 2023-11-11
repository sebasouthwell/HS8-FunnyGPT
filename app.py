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

    #Sidebar inputs are sent to dataset

    cs_body()
    return None


def cs_sidebar():

    sizeSample = st.sidebar.slider("Select sample size: ", min_value=1, max_value=100, value=1)
    seed_input = st.sidebar.text_area("Enter Seed: ", "0")
    try:
        int(seed_input)
        if len(str(seed_input)) != 10:
            st.sidebar.text("Seed must be 10 digits")
        else:
            st.sidebar.text("Success")
    except:
        st.sidebar.text("Error: Only accept integers")

    return sizeSample, seed_input


##########################
# Main body
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
