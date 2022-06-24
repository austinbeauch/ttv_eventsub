import os
from pprint import pprint
from twitchAPI import Twitch, EventSub

import modules

event_handler = modules.event_handler.Handler()


async def handle_event(data):
    event_handler(data)


if __name__ == "__main__":
    PORT = 6001
    TARGET_USERNAME = 'beauch30'
    WEBHOOK_URL = modules.ngrok_handler.init_ngrok(PORT)
    APP_ID = os.getenv("twitch_client_ID")
    APP_SECRET = os.getenv("twitch_client_secret")

    twitch = Twitch(APP_ID, APP_SECRET)
    twitch.authenticate_app([])
    uid = twitch.get_users(logins=[TARGET_USERNAME])
    user_id = uid['data'][0]['id']

    hook = EventSub(WEBHOOK_URL, APP_ID, PORT, twitch)
    hook.unsubscribe_all()
    hook.start()

    print('Subscribing to hooks...')
    hook.listen_channel_points_custom_reward_redemption_add(user_id, handle_event)

    try:
        input('press Enter to shut down...')
    finally:
        hook.stop()
    print('done')

