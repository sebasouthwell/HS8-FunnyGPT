import replicate
import requests
import time
class ReplicateHandler:
    def __init__(self,api_key):
        self.api_key = api_key
        self.url = "https://api.replicate.com/v1/predictions"
        self.imageURLCollection = []
        self.current = None
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        self.payload = {
            "version": "2e3975b1692cd6aecac28616dba364cc9f1e30c610c6efd62dbe9b9c7d1d03ea",
            "input": {
                "prompt": "Example",
                "n_predictions": 1,
                "show_clip_score": False
            }
        }

    def dalle_mini(self, prompt,prompt_identifier):
        self.payload["input"]["prompt"] = prompt
        response = requests.post(self.url, headers=self.headers, json=self.payload)
        self.current = Task(response.json(),self,prompt_identifier)
        return self.current

    def check_status(self,id):
        url = f"https://api.replicate.com/v1/predictions/{id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    
class Task:
    def __init__(self,doc_response,replicate_handler,prompt_identifier):
        self.id = doc_response["id"]
        self.prompt = doc_response["input"]["prompt"]
        self.status = doc_response["status"]
        self.status_url = doc_response["urls"]["get"]
        self.image_url = None
        self.replicate_handler = replicate_handler
        self.prompt_identifier = prompt_identifier

    def update_status(self,doc_response):
        json_check = self.replicate_handler.check_status(self.id)
        # If "The initial connection between Cloudflare's network and the origin web server timed out. As a result, the web page can not be displayed."
        # is returned, then the API is down. This is a temporary fix.
        if "The initial connection between Cloudflare's network and the origin web server timed out. As a result, the web page can not be displayed." in json_check:
            self.status = "failed"
            return
            
        self.status = json_check["status"]
        print(json_check)
        if self.status == "succeeded" and self.image_url == None:
            self.image_url = json_check["output"][0]["image"]

    def update_loop(self):
        while self.status != "succeeded":
            time.sleep(2) # Prevents spamming the API
            self.update_status(self.replicate_handler.check_status(self.id))
        return self.image_url