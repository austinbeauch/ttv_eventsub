import os
import re
import json
import socket

import bridge


def connect(token, channel):
    server = 'irc.chat.twitch.tv'
    port = 6667
    s = socket.socket()
    s.connect((server, port))
    s.send(f"PASS {token}\n".encode('utf-8'))
    s.send(f"NICK beauch30_bot\n".encode('utf-8'))
    s.send(f"JOIN {channel}\n".encode('utf-8'))
    return s


class ChatBot:
    # HUES = {'red': 0, 'yellow': 10000, 'green': 20000, 'cyan': 35000, 'blue': 45000, 'purple': 49152, 'pink': 57500}
    TOKEN = f'oauth:{os.getenv("oauth_token")}'
    CHANNEL = '#beauch30'

    def __init__(self):

        with open("colour_profiles.json", "r") as read_file:
            self.hues = json.load(read_file)

        self.sock = connect(self.TOKEN, self.CHANNEL)
        self.hue_bridge = bridge.Bridge()

    def send_chat(self, message, channel='#beauch30'):
        self.sock.send(f'PRIVMSG {channel} :{message}\r\n'.encode('utf-8'))
        print("Sent", message)

    def lights(self, message):
        # try for english name colour
        colour_in = re.search("!lights ([a-zA-Z]+).*", message)
        value_in = re.search("!lights ([0-9]{1,5}).*", message)

        if colour_in:
            key = colour_in.group(1)
            try:
                if key in self.hue_bridge.name_scene_dict:
                    scene_id = self.hue_bridge.name_scene_dict[key]
                    self.hue_bridge.set_scene(scene_id)
                    return

                profile = self.hues[key]
                if isinstance(profile, int):
#                     self.hue_bridge.hue(profile)
                    self.hue_bridge.set_group_setting("hue", profile)
                elif isinstance(profile, list):
                    self.hue_bridge.full_profile(profile)
            except KeyError: 
                print("What idiot spelt that colour wrong")

        # try for hue integer value
        elif value_in:
            hue = value_in.group(1)
            self.hue_bridge.hue(hue)

        # message only had !lights, send help command 
        else:
            helper = "Use '!lights ___' with one of these profiles: " + " ".join(list(self.hues.keys()))
            self.send_chat(helper)

    def add_profile(self, message):
        add_pattern = "!add ([a-zA-Z]+) ([0-9]{1,5}).*"
        add_in = re.search(add_pattern, message)
        name = add_in.group(1)
        value = add_in.group(2)
        self.hues[name] = int(value)

        with open("colour_profiles.json", "w") as write_file:
            json.dump(self.hues, write_file)

    def remove_profile(self, message):
        remove_pattern = "!remove ([a-zA-Z]+)"
        remove_in = re.search(remove_pattern, message)
        name = remove_in.group(1)
        try:
            self.hues.pop(name)
            with open("colour_profiles.json", "w") as write_file:
                json.dump(self.hues, write_file)

        except KeyError:
            print(f"Key {name} does not exist.")


    def monitor(self):
        try:
            print("Listening...")
            while True:
                resp = self.sock.recv(2048).decode('utf-8')
                # print(resp)
                if resp.startswith('PING'):
                    self.sock.send("PONG\n".encode('utf-8'))

                elif len(resp) > 0:
                    raw_chat = re.search(":(.+)!.+@.+.tmi.twitch.tv PRIVMSG #(.+) :(.*)", resp)
                    if not raw_chat:
                        continue

                    chatter = raw_chat.group(1)
                    message = raw_chat.group(3)
                    print(chatter, message)

                    if message.startswith("!lights"):    
                        self.lights(message)
                    elif chatter == "beauch30" and message.startswith("!add"):
                        self.add_profile(message)
                    elif chatter == "beauch30" and message.startswith("!remove"):
                        self.remove_profile(message)

        except KeyboardInterrupt:
            self.sock.close()

def main():
    botman = ChatBot()
    botman.monitor()

if __name__ == "__main__":
    main()
