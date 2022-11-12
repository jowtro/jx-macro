from playsound import playsound
from classes.action import Action
import pyautogui
from pyautogui import sleep
from helper.action import action

from helper.file_helper import parse_path


class Fire(Action):
    def __init__(self, name="Mining"):
        super().__init__(name)

    @action
    def burn_log(self):
        try:
            t = 0.15
            log_img = "./src/assets/log_osrs.png"
            pos = Fire.find_image("./src/assets/tinderbox.png")
            sleep(t)
            if pos is None:
                playsound(parse_path("./src/assets/fail.mp3"))
                exit()
            pos_log = Fire.find_image(log_img)
            Fire.go_click(pos[0] + 20, pos[1] + 20, 0.2, pyautogui.easeOutExpo)
            pos_log = Fire.find_image(log_img)
            sleep(t)
            pos_log = Fire.find_image(log_img)
            Fire.go_click(pos_log[0] + 20, pos_log[1] + 5, 0.2, pyautogui.easeOutExpo)
            sleep(t)
            pos_log = Fire.find_image(log_img)
        except Exception as ex:
            print(ex)
