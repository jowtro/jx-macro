from abc import abstractmethod, ABCMeta


class ActionUI(metaclass=ABCMeta):
    def __init__(self, name) -> None:
        self.name = name
        self.step_no = None

    def to_dict(self) -> str:
        return self.__dict__

    @abstractmethod
    def __str__(self) -> str:
        pass
