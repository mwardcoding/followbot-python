from helper import get_token, view_subscriptions, create_subscription, delete_subscription, get_ngrok_url, light_up
from flask import Flask
from flask import request, abort, redirect, url_for
import threading
import os
import json

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

with open('./data_file.json') as f:
  data = json.load(f)

token = data["token"]


current_subs = view_subscriptions(CLIENT_ID, token)
x=0
while x < current_subs["total"]:
    delete_subscription(current_subs["data"][x]["id"], CLIENT_ID, token)
    x=x+1


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        if request.json['subscription']['status'] == 'enabled':
            print(request.json['event'])
            thread = threading.Thread(target=light_up)
            thread.start()
            return "Event received", 200
        else:
            return request.json['challenge']
    else:
        return "and we're online", 200


ngrok_url = get_ngrok_url()
create_subscription(ngrok_url, CLIENT_ID, token)

