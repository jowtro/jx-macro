from classes.action_ui import ActionUI
from pynput import mouse


class MyClick(ActionUI):
    def __init__(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        super().__init__(x, y)
        self.button = button.name
        self.is_pressed = pressed
