import requests
import json
import RPi.GPIO as GPIO
from time import sleep
from dotenv import load_dotenv, find_dotenv


def get_token(client_id, client_secret):
    load_dotenv(find_dotenv())

    requests_post = requests.post('https://id.twitch.tv/oauth2/token', data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type':'client_credentials'
    })

    response_data = requests_post.json()

    token = {'token' : '{token_type} {access_token}'.format(
                        token_type=response_data["token_type"].capitalize(), 
                        access_token=response_data["access_token"])}

    print('good2go on token')
    print(token)
    
    with open("data_file.json", "w") as write_file:
        json.dump(token, write_file)



def view_subscriptions(client_id, auth_token):

    requests_get = requests.get('https://api.twitch.tv/helix/eventsub/subscriptions',
        headers = { "Client-ID": client_id,
                    "Authorization": auth_token,
                    "Content-Type": "application/json"
                    }) 
    
    response_data = requests_get.json()
    print(json.dumps(response_data, indent=2))
    return response_data



def create_subscription(ngrok_url, client_id, auth_token):
    requests_post = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions',
        headers = { "Client-ID": client_id,
                    "Authorization": auth_token,
                    "Content-Type": "application/json"
                    }, 
        json = {
                    "type": "channel.follow",
                    "version": "1",
                    "condition": {
                        "broadcaster_user_id": #Enter User ID here
                            },
                    "transport": {
                        "method": "webhook",
                        "callback": ngrok_url,
                        "secret": #"secret1234"
                    }
                })

    response_data = requests_post.json()
    print(requests_post.status_code)
    print(requests_post.headers)
    print(json.dumps(response_data, indent=2))
    
    return response_data



def delete_subscription(id, client_id, auth_token):
    requests.delete('https://api.twitch.tv/helix/eventsub/subscriptions',
    headers = { "Client-ID": client_id,
                "Authorization": auth_token,
                "Content-Type": "application/json"
                },
    params = {
        "id": id
    }) 
    

def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels/"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    for i in res_json["tunnels"]:
        if i['name'] == 'command_line':
            return i['public_url']
            break

def light_up():
    pin1 = 40

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)

    GPIO.output(pin1, True)
    sleep(10)

    GPIO.cleanup()