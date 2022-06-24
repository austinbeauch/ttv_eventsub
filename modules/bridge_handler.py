import time
from phue import Bridge as HueBridge


class Bridge:
    bridge_ip = '192.168.1.65'

    def __init__(self):
        self.bridge = HueBridge(self.bridge_ip)
        self.bridge.get_api()
        self.names = [i for i in self.bridge.get_light_objects('name')]
        self.lights = self.bridge.get_light_objects('name')
        self.light_ids = list(self.bridge.get_light_objects('id').keys())
        
        # grab all current scene names
        self.name_scene_dict = {}
        for key in self.get_scene_ids():
            name = self.get_scene_ids()[key]["name"]
            self.name_scene_dict[name] = key

    def all_on(self):
        self.set_light(on=True)
            
    def brightness(self, bri):
        self.set_lights(bri=bri)

    def saturation(self, sat):
        self.set_lights(sat=sat)

    def hue(self, hue):
        self.set_lights(hue=hue)
        
    def execute(self, hue, bri, sat):
        self.set_lights(on=True, bri=bri, hue=hue, sat=sat)
            
    def get_scene_ids(self):
        return self.bridge.get_scene()

    def set_scene(self, scene_id, group=1):
        self.bridge.activate_scene(group, scene_id)
        
    def set_lights(self, **kwargs):
        """
        Main function for all light control. Main arguments include param setting: str -> hue, bri, sat, on
        """
        self.bridge.set_light(self.light_ids, kwargs)
        
    def set_group_setting(self, setting, hue, group=1):
        """
        param setting: str -> hue, bri, sat, on
        """
        self.bridge.set_group(group, setting, hue)
        
    def blink(self, timer=3, transition=1):
        start = time.time()
        switch = True
        while time.time() - start < timer:
            self.set_lights(on=switch, bri=254, transitiontime=transition)
            switch = not switch
        self.set_lights(on=True, bri=254, transitiontime=1)
