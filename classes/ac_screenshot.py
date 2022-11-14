from classes.mouse_ui import MouseUI


class AcScreenshot(MouseUI):
    def __init__(self, x: int, y: int, filepath: str) -> None:
        super().__init__(x, y)
        self.ss_filepath = filepath
