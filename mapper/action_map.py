from classes.ac_screenshot import AcScreenshot
from classes.ac_wait import AcWait
from classes.action_ui import ActionUI
from classes.my_click import MyClick
from pynput import  mouse


class ActionMap:
    @staticmethod
    def map(action_dict: dict) -> ActionUI:
        match action_dict["name"]:
            case "Click":
                return MyClick(action_dict["x"],action_dict["y"], mouse.Button[action_dict["button"]], action_dict["is_pressed"])
            case "FindImgClick":
                return AcScreenshot(action_dict["ss_filepath"], action_dict["button"])
            case "Wait":
                return AcWait(action_dict["wait"])