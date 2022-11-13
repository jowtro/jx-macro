from datetime import datetime, timedelta


class Macro():
    """
    docstring
    """

    def __init__(self, max_iterations=9):
        self.MAX_ITERATIONS = max_iterations
        self.iterations = 0
        self.time_to_action = datetime.now()

    def add_iterations(self, val):
        self.iterations += val

    def set_iterations(self, val):
        self.iterations = val
    
    def get_iterations(self):
        return self.iterations

    def set_MAX_ITERATIONS(self, val):
        self.MAX_ITERATIONS = val

    def get_MAX_ITERATIONS(self):
        return self.MAX_ITERATIONS

    def get_time_to_act(self):
        return self.time_to_action

    def set_time_to_act(self,dt):
        self.time_to_action = dt
