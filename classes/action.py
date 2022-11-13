from classes.macro import Macro
import pyautogui
from python_imagesearch.imagesearch import imagesearch

from helper.file_helper import parse_path


class Action(Macro):

    def __init__(self, name="mining"):
        super().__init__()
        self.name = name

    @staticmethod
    def move_to(pos_x, pos_y, time=1, style=pyautogui.easeInSine):
        pyautogui.moveTo(pos_x, pos_y, time, style)

    @staticmethod
    def go_click(pos_x, pos_y, time, style):
        """move the mouse to the pos and click

        Args:t
            pos_x ([int]): x pos
            pos_y ([int]): y pos
            time ([int]): eg:. 2 seconds
            style ([pyautogui.function]): eg:.pyautogui.easeInBack
        """
        pyautogui.moveTo(pos_x, pos_y, time, style)
        pyautogui.click()

    @staticmethod
    def go_right_click(pos_x, pos_y, time, style):
        """move the mouse to the pos and click

        Args:t
            pos_x ([int]): x pos
            pos_y ([int]): y pos
            time ([int]): eg:. 2 seconds
            style ([pyautogui.function]): eg:.pyautogui.easeInBack
        """
        pyautogui.moveTo(pos_x, pos_y, time, style)
        pyautogui.rightClick()

    @staticmethod
    def find_image(image_path):
        """Find an image on screen

        Args:
            image_path ([str]): [file path]

        Returns:
            list[int]: [x,y]
        """
        pos = imagesearch(parse_path(image_path))
        if pos[0] != -1:
            return pos
        else:
            return None

    @staticmethod
    def has_found_img(pos):
        if pos:
            return True
        else:
            return False
