import json
import requests
class MongoHandler:
    def __init__(self,apiKey,collection,database,datasource):
        self.apiKey = apiKey
        self.collection = collection
        self.database = database
        self.datasource = datasource
        self.default_dict = {
            "collection": collection,
            "database": database,
            "dataSource" : datasource,
        }
        self.headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': apiKey,
        }
    
    def find(self,filter,limit=-1,no_delete=True):
        find_dict = self.default_dict
        if no_delete:
            filter = {
                **filter,
                "body": { "$ne": "[deleted]" }
            }
        if limit != -1:
            find_dict = {
                **find_dict,
                "limit": limit
            }
        payload = json.dumps({
            **find_dict,
            "filter": filter
        })
        url = "https://europe-west1.gcp.data.mongodb-api.com/app/data-eyiyj/endpoint/data/v1/action/find"
        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)['documents']

    def aggregate(self,filter):
        aggregate_dict = self.default_dict
        aggregate_payload = json.dumps({
            **aggregate_dict,
            'pipeline': filter
        })
        url = "https://europe-west1.gcp.data.mongodb-api.com/app/data-eyiyj/endpoint/data/v1/action/aggregate"
        print(aggregate_payload)
        response = requests.request("POST", url, headers=self.headers, data=aggregate_payload)
        return json.loads(response.text)['documents']
        
    def extract_bodylist(self,documents):
        bodies = []
        for v in documents:
            bodies.append(v['body'])
        return bodies