import streamlit as st
from pathlib import Path
import base64
import requests
import json
# Initial page config
request_header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

global ip
global api_resp
global imageProduction
api_resp = {}
imageProduction = False
text_area = None
ip = 'http://localhost:5000'
st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    response = requests.get(ip+'/subreddit_list')
    allSubreddits = response.json()['subreddit_list']
    cs_body()
    cs_sidebar(allSubreddits) 
    return None




def cs_sidebar(subredditList):

    sizeSample = st.sidebar.slider("Select sample size: ", min_value=1, max_value=40, value=10)
    imageOutput = st.sidebar.checkbox("Would you like an image output ")
    selectedReddits = st.sidebar.multiselect("Select your subreddits:", subredditList)

    seedInput = st.sidebar.text_area("Enter Seed: ", "12345")
    try:
        int(seedInput)
        if len(str(seedInput)) < 5:
            st.sidebar.text("Seed must be at least 5 digits")
    except:
        st.sidebar.text("Error: Only accept integers")

    button_clicked2 = st.sidebar.button("Generate GPT response")
    if button_clicked2:
        postData(sizeSample, imageOutput, selectedReddits, seedInput)

def postData(sizeSample, imageOutput, selectedReddits, seedInput):
    data = {"size-sample": sizeSample, "image-output": imageOutput, "selected-reddits": selectedReddits, "seed-inputs": seedInput}
    body = {
    "selection_size": sizeSample,
    "subreddits": selectedReddits,
    "image_required": imageOutput,
    "seed": seedInput
    }
    imageProduction = imageOutput
    data = json.dumps(body)
    response = requests.post(ip+'/generate', data, headers=request_header).json()
    api_resp = response
    # list of selected subreddits stitched together in one string in one line
    selectedSubreddits = ', '.join(selectedReddits)
    st.session_state["text"] = st.text_input('GPT Reddit DALL_E Summary for ' + selectedSubreddits  +': ', response['gpt_response'])
    if imageOutput:
       image_url = response['image_url']
       st.session_state["text"] = st.image(image_url, caption='DALL-E Generated from Reddit', use_column_width=True)
    return None


##########################
# Main body
##########################
def create_bar_chart(data):
    st.bar_chart(data)
    return None

def get_image(): #function to generate 
    document = collection.find_one()  # You might want to add a query to retrieve a specific document
    if document:
        image_url = document.get("image_url", "")
        # Display the image
        if image_url:
            st.image(image_url, caption='Generated Image', use_column_width=True)
        else:
            st.warning("No image URL found in the database.")
    else:
        st.error("Error retrieving data from MongoDB.")

 #   response = requests.gets()
 #   external_image_url = 
 #   st.image(external_image_url, caption='Generated Image', use_column_width=True)
    return

def get_graph_data():
    body = {
        'data_set_1' : [1,2,3,4,5,6,7],
        'data_set_2' : [10,12,13,4,15,9,7]
    }
    data = json.dumps(body)
    response = requests.post(ip+'/generate', data, headers=request_header)
    return


def cs_body():
    #graph_data = {
   #'Variable1': get_graph_data()[0],
   # 'Variable2': get_graph_data()[1] #example data
  #  }
    #st.bar_chart(graph_data)
    text = ''
    st.markdown("# GPT-3 Subreddit Merger and DALL-E")
    if 'gpt_response' in api_resp:
        text = (api_resp['gpt_response'])
    if "text" not in st.session_state:
        st.session_state["text"] = ""
    st.session_state["text"]
    return None

# Run main()

if __name__ == '__main__':
    main()