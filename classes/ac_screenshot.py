from classes.action_ui import ActionUI


class AcScreenshot(ActionUI):
    def __init__(self, filepath: str, button: str) -> None:
        super().__init__(name="FindImgClick")
        self.button = button
        self.ss_filepath = filepath

    def __str__(self) -> str:
        return f"Find Image and Click: {self.ss_filepath}s"
