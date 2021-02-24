import os
import requests

from pprint import pprint
from pyngrok import ngrok
from flask import Flask, request, Response

import bridge
from chat import ChatBot

app = Flask(__name__)

HUES = {'red': 0, 'yellow': 10000, 'green': 20000, 'cyan': 35000, 'blue': 45000, 'purple': 49152, 'pink': 57500}
hue_bridge = bridge.Bridge()
    
@app.route('/', methods=['POST'])
def incoming_notification():
    pprint(request.json)
    
    # if it's a callback from the server for authentication
    if "challenge" in request.json:
        print("Got challenge, returning...")
        return request.json["challenge"]
    
    elif 'event' in request.json:
        reward_name = request.json['event']["reward"]["title"]
        try:
            hue = HUES[reward_name.lower()]
            hue_bridge.set_group_setting("hue", hue)
        except KeyError:
            scene_id = hue_bridge.name_scene_dict[reward_name]
            hue_bridge.set_scene(scene_id)
        
        return Response(status=200)
    
    else:
        return Response(status=502)

try:
    app.run()
except KeyboardInterrupt:
    print("Quitting app loop")



