import os
import time
import requests
from flask import Flask, request, Response
from pprint import pprint
from pyngrok import ngrok


def init_ngrok(port=5000):
    print("Opening ngrok tunnel...")
    ngrok_tunnel = ngrok.connect(port)
    tunnels = ngrok.get_tunnels()
    https_url = tunnels[1].public_url if tunnels[1].public_url.startswith("https") else tunnels[0].public_url
    print("Opened at", https_url)
    return https_url


def renew_eventhub_subscriptions(https_url, sub_type="channel.channel_points_custom_reward_redemption.add"):
    print("Creating eventhub subscription...")
    print(https_url)
    
    subscription_data = {
        "type": sub_type,
        "version": "1",
        "condition": {
            "broadcaster_user_id": "181279574"
        },
        "transport": {
            "method": "webhook",
            "callback": https_url,
            "secret": "al4kd85kd832"
        }
    }
    
    headers = {'Client-ID': os.getenv("twitch_client_ID"),
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {os.getenv("app_access_token")}'}
    
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    
    resp = requests.post(url, json=subscription_data, headers=headers)
    
    pprint(resp.json())
    
    # need to sleep for our local server to return the challenge... I don't know why and I don't like it
    time.sleep(5)


def eventhub_unsubscribe(sub_id=None):
    eventhub_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    headers = {'Client-ID': os.getenv("twitch_client_ID"),
           'Authorization': f'Bearer {os.getenv("app_access_token")}'}
    
    # list eventhub subscriptions
    response = requests.get(eventhub_url, headers=headers)
    
    # unsub from a single service
    if sub_id is not None:
        del_response = requests.delete(eventhub_url, data={"id": sub}, headers=headers)
    
    # unsubscribe from all subscriptions 
    else:
        for sub in response.json()['data']:  
            del_response = requests.delete(eventhub_url, data={"id": sub['id']}, headers=headers)
            print(f"Deleting {sub['id']}: {del_response.status_code}")

        
if __name__ == "__main__":
    ngrok_url = init_ngrok()
    renew_eventhub_subscriptions(ngrok_url)
