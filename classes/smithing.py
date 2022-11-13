from classes.action import Action
from pyautogui import sleep
import pyautogui


class Smithing(Action):

    def __init__(self, name="Mining", forge=[0, 0], anvil=[0, 0]):
        super().__init__(name)
        self.forge = forge
        self.anvil = anvil
        self.forge_found = False
        self.anvil_found = False
        # TODO add function to scan dir looking for files with a prefix
        self.image_found = False

    def find_and_set_forge(self):
        pos = super().find_image("./assets/forge1.png")
        # has found
        if pos:
            self.forge[0] = pos[0] + 30
            self.forge[1] = pos[1] + 15
            self.forge_found = True
        else:
            self.forge_found = False
            print("forge_found not found exception !")

    def find_and_set_anvil(self):
        pos = super().find_image("./assets/anvil.png")
        # has found
        if pos:
            self.anvil[0] = pos[0] + 30
            self.anvil[1] = pos[1] + 15
            self.anvil_found = True
        else:
            self.anvil_found = False
            print("anvil not found exception !")

    def look_for_bonus_xp(self):
        for img in self.list_burst_xp:
            pos_xp = super().find_image(img)
            if super().has_found_img(pos_xp):
                self.image_found = True
                sleep(1)
                super().go_click(pos_xp[0], pos_xp[1],
                                 2, pyautogui.easeInBounce)
            else:
                self.image_found = False
