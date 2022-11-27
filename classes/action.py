from classes.macro import Macro
import pyautogui
from pyautogui import Point
from helper.file_helper import parse_path


class Action(Macro):
    def __init__(self, form, name="mining"):
        super().__init__()
        self.name = name
        self.form = form

    @staticmethod
    def move_to(pos_x: int, pos_y: int, time=1, style=pyautogui.easeInSine):
        pyautogui.moveTo(pos_x, pos_y, time, style)

    @staticmethod
    def go_click(pos_x: int, pos_y: int, time: float, button: str, style):
        """move the mouse to the pos and click

        Args:t
            pos_x ([int]): x pos
            pos_y ([int]): y pos
            time ([int]): eg:. 2 seconds
            style ([pyautogui.function]): eg:.pyautogui.easeInBack
        """
        pyautogui.moveTo(pos_x + 5, pos_y + 5, time, style)
        pyautogui.click() if button == "left" else pyautogui.rightClick()

    @staticmethod
    def find_image(image_path: str, min_time=5):
        """Find an image on screen

        Args:
            image_path ([str]): [file path]

        Returns:
            list[int]: [x,y]
        """
        try:
            img = pyautogui.locateOnScreen(parse_path(image_path), min_time)
            pos = pyautogui.center(img)
            if pos is None:
                return None
            else:
                return pos
        except Exception as ex:
            print("Image not Found")

    @staticmethod
    def has_found_img(pos):
        if pos:
            return True
        else:
            return False

    def find_image_click(
        self, image_path: str, button: str, time: float, style=pyautogui.easeInBack
    ):
        """Find an image on screen

        Args:
            image_path ([str]): [file path]

        Returns:
            list[int]: [x,y]
        """
        pos = Action.find_image(parse_path(image_path), time)
        if pos is None:
            return None

        Action.go_click(pos.x, pos.y, time, button, style)

    def find_image_click_all(
        self, image_path: str, button: str, time: float, style=pyautogui.easeInBack
    ):
        while self.form.playing:
            pos = self.find_image(image_path)
            if pos is None:
                return None
            print("found another image.")
            Action.go_click(pos.x, pos.y, time, button, style)
            pyautogui.sleep(0.05)

    @staticmethod
    def wait(seconds: float):
        pyautogui.sleep(seconds)
