from pynput import mouse
from classes.mouse_ui import MouseUI


class MyClick(MouseUI):
    def __init__(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        super().__init__(x, y)
        self.button = button.name
        self.is_pressed = pressed
        
    def __str__(self) -> str:
        return f"Click [{str(self.x)},{str(self.y)}]"
