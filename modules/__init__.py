from . import bridge_handler
bridge = bridge_handler.Bridge()

HUES = {'red': 0, 'yellow': 10000, 'green': 20000, 'cyan': 35000, 
        'blue': 45000, 'purple': 49152, 'pink': 57500}

from . import response_handlers

FOLLOW = "channel.follow"
SUB = "channel.subscribe"
CHANNEL_POINTS = "channel.channel_points_custom_reward_redemption.add"

event_handler = {
    FOLLOW :         response_handlers.blink,
    SUB:             response_handlers.blink,
    CHANNEL_POINTS : response_handlers.channel_points_handler
}

from . import ngrok_handler
