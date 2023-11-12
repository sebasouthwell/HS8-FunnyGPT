# Generate a class handler for the ChatGPT 3.5 API
import json
import requests
class GPTHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

    def generate_dall_e_query(self, input_message):
        params = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarises the whole input query, into one funny & specific painting dall-e prompt, no exceptions:"},
                {"role": "user", "content": input_message}
            ]
        }
        response = requests.post(self.api_url, data=json.dumps(params), headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            for message in data["choices"]:
                return message['message']['content']
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return None
