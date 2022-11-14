class ActionUI:
    def __init__(self) -> None:
        self.step_no = None

    def to_dict(self) -> str:
        return self.__dict__