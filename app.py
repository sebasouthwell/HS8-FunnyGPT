import streamlit as st
from pathlib import Path
import base64
import requests
import json
# Initial page config
st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():

    allSubreddits = ["Donotmove", "yesplease"]
    cs_sidebar(allSubreddits) 
    
    cs_body()
    return None


def cs_sidebar(subredditList):

    sizeSample = st.sidebar.slider("Select sample size: ", min_value=1, max_value=100, value=1)
    imageOutput = st.sidebar.checkbox("Would you like an image output ")
    selectedReddits = st.sidebar.multiselect("Select your subreddits:", subredditList)

    seedInput = st.sidebar.text_area("Enter Seed: ", "0")
    try:
        int(seedInput)
        if len(str(seedInput)) != 10:
            st.sidebar.text("Seed must be 10 digits")
    except:
        st.sidebar.text("Error: Only accept integers")

    button_clicked2 = st.sidebar.button("Generate GPT response")
    if button_clicked2:
        postData(sizeSample, imageOutput, selectedReddits, seedInput)

def postData(sizeSample, imageOutput, selectedReddits, seedInput):
    url = False
    data = {"size-sample": sizeSample, "image-output": imageOutput, "selected-reddits": selectedReddits, "seed-inputs": seedInput}

    response = requests.post(url, json.dumps(data))


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


def get_image(): #function to generate 
    response = requests.get("https://api.example.com/data")
    data = response.json()
    return data["URL"] #returns image URL

def get_graph_data():
    #return (json.load(requests.get("https://api.example.com/data")))["Array1"] , (json.load(requests.get("https://api.example.com/data")))["Array2"]
    return [1,2,3,4,5,6] , [12,10,14,9,7,21] 

def get_GPT_data():
    #return (json.load(requests.get("https://api.example.com/data")).json)["GPT_text"]
    return "Hello World"



def cs_body(inputList):
    


    GPT_text = get_GPT_data()
    graph_data = {
    'Variable1': get_graph_data()[0],
    'Variable2': get_graph_data()[1] #example data
    }
    st.bar_chart(graph_data)
    display_text_in_textbox(GPT_text)    
    #display_image_from_sdiffusion(url) #<---------- image url from side menu here
    return None

# Run main()

if __name__ == '__main__':
    main()
