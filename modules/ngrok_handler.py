import os
import time
import random
import string
import requests

from pyngrok import ngrok 


def start_ngrok(subs):
    # sleep to ensure flask server starts before making a request
    time.sleep(5)
    # oauth_status = test_oauth()
    # if oauth_status:
    ngrok_url = init_ngrok()
    create_eventhub_subscriptions(ngrok_url, subs)
    # else:
        # print("OAuth token needs to be set. Press ctrl+c to exit.")


# def test_oauth():
#     # scope ="analytics:read:extensions analytics:read:games bits:read channel:edit:commercial channel:manage:broadcast channel:manage:extensions channel:manage:redemptions channel:manage:videos channel:read:editors channel:read:hype_train channel:read:redemptions channel:read:subscriptions clips:edit moderation:read user:edit user:read:blocked_users user:manage:blocked_users user:read:broadcast channel:moderate chat:edit chat:read whispers:read whispers:edit"

#     # try and get subscriptions to see if twitch_access_token is valid
#     url = "https://api.twitch.tv/helix/eventsub/subscriptions"
#     headers = {'Client-ID': os.getenv("twitch_client_ID"),
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {os.getenv("twitch_access_token")}'}
#     response = requests.get(url, headers=headers)

#     if "error" in response.json().keys():
#         print("OAuth token not set. Requesting a new one...")
#         # print(scope)
#         oauth_data = {
#             "client_id": os.getenv("twitch_client_ID"),
#             "client_secret": os.getenv("twitch_client_secret"),
#             "grant_type": "client_credentials",
#             # "scope": scope
#         }
#         oauth_url = "https://id.twitch.tv/oauth2/token"

#         req = requests.post(oauth_url, json=oauth_data)
#         print(req.json())

#         if req.status_code == 200:
#             print("Success!")
#             print("The access token will be written to a file.")
#             print("Keep this secret, and reset your environment variable <twitch_access_token>, then restart your terminal.")
#             token = req.json()["access_token"]

#             with open('token.txt', 'w') as f:
#                 f.write(token + "\n")

#         else: 
#             print("Error retrieving new access token.")
        
#         return False
    
#     return True


def init_ngrok(port=5000):
    print("Opening ngrok tunnel...")
    ngrok_tunnel = ngrok.connect(port)
    tunnels = ngrok.get_tunnels()
    https_url = tunnels[1].public_url if tunnels[1].public_url.startswith("https") else tunnels[0].public_url
    print("Opened at", https_url)
    return https_url


def create_eventhub_subscriptions(https_url, subscriptions):    
    for sub_type in subscriptions:
        subscription_data = {
            "type": sub_type,
            "version": "1",
            "condition": {
                "broadcaster_user_id": "181279574"
            },
            "transport": {
                "method": "webhook",
                "callback": https_url,
                "secret": "".join(random.choices(string.ascii_lowercase + string.digits, k=15))
            }
        }        

        url = "https://api.twitch.tv/helix/eventsub/subscriptions"
        headers = {'Client-ID': os.getenv("twitch_client_ID"),
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("twitch_access_token")}'}

        req = requests.post(url, json=subscription_data, headers=headers)
        if req.status_code == 202:
            print(f"Successfully created subscription for {sub_type}")
        else:
            print(f"Error for sub type {sub_type}")


def eventhub_unsubscribe(sub_id=None):
    eventhub_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    headers = {'Client-ID': os.getenv("twitch_client_ID"),
           'Authorization': f'Bearer {os.getenv("twitch_access_token")}'}
    
    # list eventhub subscriptions
    response = requests.get(eventhub_url, headers=headers)
    
    if sub_id is not None:  # unsub from a single service
        del_response = requests.delete(eventhub_url, data={"id": sub_id}, headers=headers)
    else:  # unsubscribe from all subscriptions 
        if "error" in response.json().keys():
            return

        for sub in response.json()['data']:  
            del_response = requests.delete(eventhub_url, data={"id": sub['id']}, headers=headers)
            print(f"Deleting {sub['id']}: {del_response.status_code}")

        
if __name__ == "__main__":
    ngrok_url = init_ngrok()
    create_eventhub_subscriptions(ngrok_url)
