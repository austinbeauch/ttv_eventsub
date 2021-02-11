from phue import Bridge as HueBridge


class Bridge:
    bridge_ip = '192.168.1.85'

    def __init__(self):
        self.bridge = HueBridge(self.bridge_ip)
        self.bridge.get_api()
        self.names = [i for i in self.bridge.get_light_objects('name')]
        self.lights = self.bridge.get_light_objects('name')

    def brightness(self, bri):
        for light in self.names:
            self.bridge.set_light(light, 'bri', bri)

    def saturation(self, sat):
        for light in self.names:
            self.lights[light].saturation = sat

    def hue(self, hue):
        for light in self.names:
            self.lights[light].hue = hue

    def execute(self, hue, bri, sat):
        for light in self.names:
            self.lights[light].hue = hue
            self.bridge.set_light(light, 'bri', bri)
            self.lights[light].saturation = sat

    def full_profile(self, hues):
        for light, hue in zip(self.names, hues):
            self.lights[light].hue = hue
