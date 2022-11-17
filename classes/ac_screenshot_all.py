from classes.ac_screenshot import AcScreenshot
from classes.action_ui import ActionUI


class AcScreenshotAll(AcScreenshot):
    def __init__(self, filepath: str, button: str) -> None:
        super().__init__(filepath, button)
        self.loop = True
        
    def __str__(self) -> str:
        return f"Find Image and Click and loop: {self.ss_filepath}s"
