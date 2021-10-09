from playsound import playsound
import threading
import keyboard
import flask
import json
import os
from pygame.constants import OPENGL
import pygame.mixer
from flask import request

APPDATA = os.getenv("APPDATA").replace("\\", "/")
template = """<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>KeySound Config</title> <style>body{font-family: 'Montserrat', sans-serif;}</style> <script>function change_volume(){let element=document.querySelector("#volume"); let label=document.querySelector("#volumeLabel"); label.textContent=element.value;}</script></head><body> <form action="change" method="get"> <div> Volume <input type="range" id="volume" name="volume" min="0" max="100" value="{{volume}}" onchange="change_volume()"> <label for="volume" id="volumeLabel">{{volume}}</label> </div><div> Sound <input type="text" name="sound" value="{{sound}}"> </div><div> Enable <input type="checkbox" name="work" checked> </div><button type="submit">Apply</button> </form> <link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"></body></html>"""

server = flask.Flask(__name__)

with open(APPDATA + "/KeySound/app.config") as config_path:
    config = json.load(config_path)

settings = {"sound": config["sound"].replace("%APPDATA%", APPDATA), "volume": config["volume"], "work": "1"}

pygame.mixer.init()
pygame.mixer.music.set_volume(float(settings["volume"]))
pygame.mixer.music.load(settings["sound"])

def keyhook(event):
    if event.event_type == "down":
        if settings["work"] == "1":
            pygame.mixer.music.play()


@server.route("/change/volume", methods=["GET"])
def __change_volume():
    value = request.args.get("value")
    settings["volume"] = float(value)
    with open(APPDATA + "/KeySound/app.config", "w") as config_path:
        json.dump(settings, config_path)
    
    pygame.mixer.music.set_volume(float(value))

    return "0"

@server.route("/change/sound", methods=["GET"])
def __change_sound():
    value = request.args.get("value")
    settings["sound"] = value
    with open(APPDATA + "/KeySound/app.config", "w") as config_path:
        json.dump(settings, config_path)

    pygame.mixer.music.load(settings["sound"])

    return "0"

@server.route("/change/work", methods=["GET"])
def __change_work():
    value = request.args.get("value")

    settings["work"] = value

    return "0"

@server.route("/change", methods=["GET"])
def __change():
    if flask.request.args.get("work"):
        settings["work"] = "1"
    else:
        settings["work"] = "0"

    if len(flask.request.args.get("sound")) > 2:
        settings["sound"] = flask.request.args.get("sound")
        pygame.mixer.music.load(flask.request.args.get("sound"))

    settings["volume"] = int(flask.request.args.get("volume")) / 100
    pygame.mixer.music.set_volume(int(flask.request.args.get("volume")) / 100)

    with open(APPDATA + "/KeySound/app.config", "w") as config_path:
        json.dump(settings, config_path)

    return flask.redirect("/edit")
    

@server.route("/")
def __index():
    return flask.redirect("/edit")

@server.route("/edit")
def __edit():
    return flask.render_template_string(template, sound=settings["sound"], volume=float(settings["volume"])*100)


def main():
    threading.Thread(target=server.run, args=("127.0.0.1", 4445), daemon=True).start()

    keyboard.hook(keyhook)
    keyboard.wait()


main()
