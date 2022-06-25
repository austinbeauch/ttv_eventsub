from . import bridge_handler

class Handler:
    FOLLOW = "channel.follow"
    SUB = "channel.subscribe"
    CHANNEL_POINTS = "channel.channel_points_custom_reward_redemption.add"

    HUES = {'red': 0, 'yellow': 10000, 'green': 20000, 'cyan': 35000, 
            'blue': 45000, 'purple': 49152, 'pink': 57500}

    def __init__(self, group=None):
        self.bridge = bridge_handler.Bridge(group)
        self.subscriptions = [self.FOLLOW, self.SUB, self.CHANNEL_POINTS]

    def __call__(self, request):
        self.handle_request(request)

    async def handle_request(self, request):
        event_type = request["subscription"]["type"]

        if event_type == self.CHANNEL_POINTS:
            await self.channel_points(request)

        elif event_type == self.FOLLOW or event_type == self.SUB:
            await self.bridge.blink()


    async def channel_points(self, request):
        reward = request['event']["reward"]["title"].lower()

        if reward in self.HUES:
            hue = self.HUES[reward.lower()]
            self.bridge.set_lights(hue=hue, on=True) 
        
        elif reward in self.bridge.name_scene_dict:
            scene_id = self.bridge.name_scene_dict[reward]
            self.bridge.set_scene(scene_id)
