import os
import shutil
import os.path
import time

try:
    APPDATA = os.getenv("APPDATA").replace("\\", "/")
    STARUP = APPDATA + "/Microsoft/Windows/Start Menu/Programs/Startup"

    if not os.path.exists(APPDATA + "/KeySound"):
        os.mkdir(APPDATA + "/KeySound")
        os.mkdir(APPDATA + "/KeySound/Sounds")


    shutil.copyfile('./build/KeySound.exe', STARUP + "/KeySound.exe")
    shutil.copyfile('./sounds/gl-tactile.mp3', APPDATA + "/KeySound/Sounds/gl-tactile.mp3")
    shutil.copyfile('./app.info', APPDATA + "/KeySound/app.info")
    shutil.copyfile('./app.config', APPDATA + "/KeySound/app.config")

    os.system(f'"{STARUP}/KeySound.exe"')

    print("Success!\nOpen http://127.0.0.1:4445 for edit KeySound")
except Exception as e:
    print("Error")
    print(e)

time.sleep(60)
