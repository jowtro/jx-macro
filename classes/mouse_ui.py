from classes.pos import Pos

class MouseUI(Pos):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("Click",x, y)
        self.step_no = None