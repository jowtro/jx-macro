from datetime import datetime, timedelta


class Interval(object):
    """It wraps a function and execute it on each interval
    """
    def __init__(self, interval=120):
        """
        Args:
            interval (int, optional): interval on which the function will be called in seconds. Defaults to 120.
        """
        self.interval = interval
        self.time_to_act = datetime.now() - timedelta(0, self.interval )

    def __call__(self, func):
        # Will only execute the function if time has passed
        def wrapper(*args, **kwargs):
            if self.time_to_act < datetime.now():
                self.time_to_act = datetime.now() + timedelta(0, self.interval )
                #print(f"DEBUG: macro tick set to next {self.interval} s")
                return func(*args, **kwargs)
        return wrapper
