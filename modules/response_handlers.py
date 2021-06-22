from flask import request

from . import bridge, HUES

def blink(response):
    bridge.blink()

def channel_points_handler(response):
    reward = request.json['event']["reward"]["title"]
    if reward.lower() in HUES:
        hue = HUES[reward.lower()]
        bridge.set_lights(hue=hue, on=True)  # Change this back to groups if needed
        # hue_bridge.set_group_setting("hue", hue)
    elif reward in bridge.name_scene_dict:
        scene_id = bridge.name_scene_dict[reward]
        bridge.set_scene(scene_id)
