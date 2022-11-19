import tkinter as tk
from typing import Any


def get_setting(val: str, param: dict) -> Any | None:
    if val in param:
        return param[val]
    else:
        return None


def set_txt_status(self, text: str):
    self.txt_status.delete("1.0", tk.END)  # Clear current contents.
    self.txt_status.insert(tk.INSERT, text)
