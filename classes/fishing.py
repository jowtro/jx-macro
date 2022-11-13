from classes.action import Action
from pyautogui import sleep
import pyautogui


class Fishing(Action):

    def __init__(self, name="Mining", forge=[0, 0], anvil=[0, 0]):
        super().__init__(name)

    def drop_cray_fish(self):
        pos = Fishing.find_image('./assets/crayfish.png')
        Fishing.go_right_click(pos[0]+20, pos[1]+20, 0.2, pyautogui.easeInOutSine)
        pos = Fishing.find_image('./assets/drop.png')
        Fishing.go_click(pos[0]+20, pos[1]+5, 0.2, pyautogui.easeInOutSine)

    def drop_trout_fish(self):
        pos = Fishing.find_image('./assets/trout_fish.png')
        Fishing.go_right_click(pos[0]+20, pos[1]+20, 0.2, pyautogui.easeInOutSine)
        pos = Fishing.find_image('./assets/drop.png')
        Fishing.go_click(pos[0]+20, pos[1]+5, 0.2, pyautogui.easeInOutSine)
