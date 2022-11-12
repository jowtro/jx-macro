#! python3
import json
from threading import Thread
import time
from tkinter import messagebox, ttk
import pyautogui
import tkinter as tk
from tkinter import Label, StringVar, Listbox, Scrollbar
from pyautogui import sleep
from pynput import keyboard, mouse
from classes.action import Action
from queue import Queue


class Pos:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class ActionUI(Pos):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.step_no = None

    def to_dict(self) -> str:
        return super().__dict__


class MyClick(ActionUI):
    def __init__(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        super().__init__(x, y)
        self.button = button.name
        self.is_pressed = pressed


class ActionForm:
    def __init__(self) -> None:
        self.position_str = None
        self.actions_list = []
        self.no_steps = 0
        self.macro = None

    def inc_steps(self):
        """increment steps by 1"""
        self.no_steps += 1

    def on_release(self, key) -> None:
        x, y = pyautogui.position()
        self.position_str = f"[{str(x).rjust(4)},{str(y).rjust(4)}]"

    def on_click(self, x, y, button: mouse.Button, pressed: bool) -> None:
        if not pressed:
            return
        click = MyClick(x, y, button, pressed)
        self.add_action(click)
        self.position_str = f"[{str(x).rjust(4)},{str(y).rjust(4)}]"

    def tk_on_click_save(self, event):
        self.write_to_file()
        messagebox.showinfo("Message", "Macro saved.")

    def tk_on_click_play(self, event):
        print("Play")
        self.read_macro()
        self.play_macro

    def add_action(self, action: ActionUI):
        self.inc_steps()
        action.step_no = self.no_steps
        self.actions_list.append(action.to_dict())

    def write_to_file(self):
        with open("teste.json", "w") as f:
            json_file = dict(steps=self.actions_list)
            f.write(json.dumps(json_file))
            f.write("\n")

    def read_macro(self):
        with open("teste.json", "r") as f:
            self.macro = json.loads(f.read())

    def play_macro(self):
        a = Action()
        for step in self.macro:
            pass


def update_gui():
    if action_ui.position_str != "":
        listbox_widget.insert(tk.END, action_ui.position_str)
    action_ui.position_str = ""
    root.after(100, update_gui)


if __name__ == "__main__":
    q = Queue()
    action_ui = ActionForm()
    root = tk.Tk(className="JXTECH")
    root.geometry("400x200")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    # BTN SAVE
    btn_save = ttk.Button(root, text="Save Macro")
    btn_save.bind("<Button-1>", action_ui.tk_on_click_save)
    btn_save.grid(column=0, row=1, sticky=tk.E, padx=5, pady=5)
    # PLAY
    btn_play = ttk.Button(root, text="Play Macro")
    btn_play.bind("<Button-2>", action_ui.tk_on_click_play)
    btn_play.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

    listbox_entries = []
    scrollbar = Scrollbar(root)
    listbox_widget = Listbox(root, yscrollcommand=scrollbar.set)
    listbox_widget.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)

    msg = StringVar()
    msg.set(f"Press any key to record x,y pos")

    label = Label(root, textvariable=msg)
    scrollbar.config(command=listbox_widget.yview)
    # ...or, in a non-blocking fashion:
    keyboard_listener = keyboard.Listener(on_release=action_ui.on_release)
    keyboard_listener.start()
    mouse_listener = mouse.Listener(on_click=action_ui.on_click)
    mouse_listener.start()

    # Collect events until released
    update_gui()
    root.mainloop()
