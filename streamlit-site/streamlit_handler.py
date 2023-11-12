import streamlit as st
from pathlib import Path
import base64
import requests
import json

class streamLitHandler:

    def __init__(self,ip)
        self.ip = ip
        self.subreddit_list =  self.get_subreddits()
        st.set_page_config(
            page_title='Streamlit cheat sheet',
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self.request_header = request_header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def get_subreddits():
        response = requests.get(ip+'/subreddit_list')
        allSubreddits = response.json()['subreddit_list']
    
        return allSubreddits
    
    def display():
        cs_sidebar(allSubreddits) 
        cs_body()

    def sidebar(self):
        self.sizeSample = st.sidebar.slider("Select sample size: ", min_value=1, max_value=40, value=10)
        self.imageOutput = st.sidebar.checkbox("Would you like an image output ")
        self.selectedReddits = st.sidebar.multiselect("Select your subreddits:", subredditList)

        self.seedInput = st.sidebar.text_area("Enter Seed: ", "12345")
        try:
            int(seedInput)
            if len(str(seedInput)) < 5:
                st.sidebar.text("Seed must be at least 5 digits")
        except:
            st.sidebar.text("Error: Only accept integers")

        self.button_clicked2 = st.sidebar.button("Generate GPT response")
        if self.button_clicked2:
            postData(sizeSample, imageOutput, selectedReddits, seedInput)

    def body(self):
        self.gpt_response = self.gpt_request()
        st.text_area("GPT Reddit DALL_E Summary", self.gpt_response['gpt_response'])
        if self.imageOutput:
            st.image(self.gpt_response['image_response'], use_column_width=True)
    return None

    def gpt_request():
        body = {
        "selection_size": self.sizeSample.value,
        "subreddits": self.selectedReddits.value,
        "image_required": self.imageOutput.value,
        }
        data = json.dumps(body)
        response = requests.post(ip+'/generate', data, headers=self.request_header)
        return 
        response = requests.get(ip+'/gpt_request')
        return response.json()