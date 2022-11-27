from classes.action_ui import ActionUI
from time import sleep


class AcWait(ActionUI):
    def __init__(self, wait_seconds: float) -> None:
        self.wait = float(wait_seconds)
        super().__init__(name="Wait")

    def __str__(self) -> str:
        return f"Wait {self.wait}s"
