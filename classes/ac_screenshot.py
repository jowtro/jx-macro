from classes.action_ui import ActionUI


class AcScreenshot(ActionUI):
    def __init__(self, filepath: str, button: str) -> None:
        self.button = button
        self.ss_filepath = filepath
