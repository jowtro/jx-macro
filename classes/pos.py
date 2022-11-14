from classes.action_ui import ActionUI

class Pos(ActionUI):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y