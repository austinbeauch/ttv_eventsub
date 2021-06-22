import threading

from pprint import pprint
from flask import Flask, request, Response

import modules

app = Flask(__name__)
event_handler = modules.event_handler.Handler()

@app.route('/', methods=['POST'])
def incoming_notification():  
    # if it's a callback from the server for authentication
    if "challenge" in request.json:
        challenge_type = request.json["subscription"]["type"]
        print(f"Returning challenge for {challenge_type}")
        return request.json["challenge"]

    else:
        pprint(request.json)
        event_type =  request.json["subscription"]["type"]
        try:
            # modules.event_handler[event_type](request.json)
            event_handler(request)
        except Exception as ex:
            print(f"Something went wrong: \n {ex}")
        return Response(status=200)
           

if __name__ == "__main__":
    try:
        # threading.Thread(target=modules.ngrok_handler.start_ngrok).start()
        threading.Thread(target=modules.ngrok_handler.start_ngrok, 
                           args=(event_handler.subscriptions,)).start() 
        app.run()
    finally:
        modules.ngrok_handler.eventhub_unsubscribe()
