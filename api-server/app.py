from flask import Flask, jsonify, request
from mongo_db import MongoHandler
from gpt_handler import GPTHandler
from replicate_handler import ReplicateHandler
from dotenv import load_dotenv
import os
import requests
import random

app = Flask(__name__)
mongoHandler = None
gpt_handler = None
replicateHandler = None
main_subreddits = None
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'No data was sent.'})
    if not data['selection_size']:
        return jsonify({'error': 'No selection size was sent.'})
    if not data['subreddits']:
        return jsonify({'error': 'No subreddits were sent.'})
    if 'image_required' not in data:
       return jsonify({'error': 'No image_required was sent.'})
    if 'seed' not in data:
       return jsonify({'error': 'No seed was sent.'})
    sample = data['selection_size']
    subreddits = data['subreddits']
    dall_e_prod = data['image_required']
    seed = data['seed']
    query = {
         "$or": [
        ]}
    for subreddit in subreddits:
         query["$or"].append({"subreddit": subreddit})
    query_match = mongoHandler.find(query,sample*2)
    # Create a random with seed
    random.seed(seed)
    query_match = random.sample(query_match, sample)
    gpt_query_array = mongoHandler.extract_bodylist(query_match)
    gpt_query_string = '\n'.join(gpt_query_array)
    if gpt_query_string == '':
          return jsonify({'error': 'No data was found.'})
    gpt_resp_string = gptHandler.generate_dall_e_query(gpt_query_string)
    if gpt_resp_string == None:
        return jsonify({'error': 'No data was found.'})
    if (dall_e_prod):
        dall_e_task = replicateHandler.dalle_mini(gpt_resp_string,1)
        image_url =  dall_e_task.update_loop()
        response = jsonify({'gpt_response': gpt_resp_string, 'image_url': image_url})
        return response
    else:
        return jsonify({'gpt_response': gpt_resp_string})

@app.route('/subreddit_list')
def subreddit_list():
    query = [
    {
        '$project': {
            '_id': 0, 
            'subreddit': 1
        }
        }
    ]
    subreddit_list = mongoHandler.aggregate(query)
    # Extract a set of unique subreddits names
    subreddit_list = set([subreddit['subreddit'] for subreddit in subreddit_list])
    # Convert the set to a list
    subreddit_list = list(subreddit_list)
    reddit_blacklist = ['sex','tits','porn','xx','girl','fap','bipolar','teen','gay','jerk','pussy','ass','futa','fet','furries','nsfw','boob','hot','hentai','fur','boner','lgbt','suicide','asmr','dyke','dating','tran','nude','feet','issues','uction','cam','who','bdsm'] 
    truereddit_list = []
    for i in subreddit_list:
        safe = True
        for j in reddit_blacklist:
            if j in i.lower():
                safe = False
                break
        if safe:
            truereddit_list.append(i)
    main_subreddits = truereddit_list
    response = jsonify({'subreddit_list': main_subreddits})
    return response

# Create a 404 page to handle incorrect routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Route not found.'})
     
if __name__ == '__main__':
   load_dotenv()
   replicateHandler = ReplicateHandler(os.getenv("REPLICATE_API_TOKEN"))
   gptHandler = GPTHandler(os.getenv("OPENAI_API_KEY"))
   mongoHandler = MongoHandler(os.getenv("MONGO_API_KEY"),os.getenv("MONGO_COLLECTION"),os.getenv("MONGO_DATABASE"),os.getenv("MONGO_DATASOURCE"))
   main_subreddits = []
   app.run()
