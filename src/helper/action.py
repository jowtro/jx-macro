def action(cls):
    """decorator that increment the interations"""

    def wrapper(self, *args, **kwargs):
        cls(self, *args, **kwargs)
        self.add_iterations(1)
        print(f"Doing action...\n{self.get_iterations()}/{self.get_MAX_ITERATIONS()}")

    return wrapper
