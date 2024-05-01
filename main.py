import os
import sys
import json
import time
import requests
import websocket
from websocket import WebSocket
from json import dumps
from server import keep_alive


status = "dnd" #online/dnd/idle

custom_status = "Sleepy" #If you don't need a custom status on your profile, just put "" instead of "youtube.com/@SealedSaucer"

usertoken = os.environ.get('token')
server_id = "1137685200244047912" # ไอดีเซิร์ฟ
channel_id = "1210834568597340180" # ไอดีช่องเสียง


if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner():
    ws_voice = WebSocket()
    ws_voice.connect("wss://gateway.discord.gg/?v=8&encoding=json")
    ws_voice.send(dumps(
        {
            "op": 2,
            "d": {
                "token": usertoken,
                "properties": {
                    "$os": "windows",
                    "$browser": "Discord",
                    "$device": "desktop"
                }
            }
        }))
    ws_voice.send(dumps({
        "op": 4,
        "d": {
            "guild_id": server_id,
            "channel_id": channel_id,
            "self_mute": True,
            "self_deaf": False, 
            "self_stream?": False, 
            "self_video": False
        }
    }))
    ws_voice.send(dumps({
        "op": 18,
        "d": {
            "type": "guild",
            "guild_id": server_id,
            "channel_id": channel_id,
            "preferred_region": "spain"
        }
    }))
    ws_voice.send(dumps({
        "op": 1,
        "d": None
    }))
    

keep_alive()
if __name__ == "__main__":
	while True:
            onliner()

