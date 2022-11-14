from classes.action_ui import ActionUI
from time import sleep


class AcWait(ActionUI):
    def __init__(self, wait_seconds: int) -> None:
        self.wait = wait_seconds
        super().__init__()