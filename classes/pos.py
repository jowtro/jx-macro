from classes.action_ui import ActionUI


class Pos(ActionUI):
    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(name=name)
        self.x = x
        self.y = y
