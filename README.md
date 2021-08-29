# ttv_bot
twitch.tv Flask application for interfacing with Twitch's EventSub API.

This repositoy consists of three main processes:

- Flask webserver hosted via an ngrok public URL for Twitch EventSub callbacks
- ngrok URL initializer along with EventSub subscription creation/deletion 
- Event callback handling, mainly focused with Philips Hue interaction 

### Usage

Main usage considerations include setting up a Twitch developer access token and Philips Hue setup. 
Access credientials are stored in Windows environment variables and accessed in `modules/ngrok_handler.py` 
with `os.getenv()`. Ensure this token has proper authorization. 
Refer to the [documentation](https://dev.twitch.tv/docs/eventsub) for more details.
For Hue integration, the the [phue](https://github.com/studioimaginaire/phue) library is required. Simply update your bridge IP in [bridge_handler.py](https://github.com/austinbeauch/ttv_bot/modules/bridge_handler.py#L6)

Customizing request handling can be done by modifying [event_handler.py](https://github.com/austinbeauch/ttv_bot/modules/event_handler.py)
