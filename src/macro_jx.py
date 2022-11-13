import json
import time
import tkinter as tk
from tkinter import BOTH, Label, Listbox, PhotoImage, Scrollbar, StringVar
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from typing import List

import pyautogui
from pynput import keyboard, mouse

from classes.action import Action
from classes.action_ui import ActionUI
from classes.my_click import MyClick
from helper.file_helper import parse_path


class ActionForm:
    def __init__(self) -> None:
        self.position_str = None
        self.actions_list = []
        self.no_steps = 0
        self.macro = None
        self.btn_save = None
        self.macro_filename = None
        self.record = False
        self.playing = False
        self.cnt = 1
        self.iterations = 2
        self.speed = 1

    def inc_steps(self):
        """increment steps by 1"""
        self.no_steps += 1

    def reset_cnt(self):
        self.cnt = 1

    def on_release(self, key: keyboard.Key) -> None:
        try:
            if key == key.esc:
                self.record = False
                self.playing = False
                self.reset_cnt()
                print("Record Stoped")
        except Exception as ex:
            print(ex)

    def on_click(self, x, y, button: mouse.Button, pressed: bool) -> None:
        if not pressed:
            return

        if not self.record:
            return
        # FIX ME ignore whole app window instead of one button
        btnx, btny = self.btn_save.winfo_rootx(), self.btn_save.winfo_rooty()
        btn_size_x = self.btn_save.winfo_width()
        btn_size_y = self.btn_save.winfo_height()
        print(
            f"{x} > {btnx} and {x} < ({btnx + btn_size_x}) and {y} > {btny} and {y} < ({btny + btn_size_y})"
        )
        print("size")
        print(btn_size_x, btn_size_y)
        print(f"btnx {btnx} btny {btny}")
        print(x > btnx)
        print(x < (x + btn_size_x))
        print(y > btny)
        print(y < (y + btn_size_y))
        # if cursor is inside save btn
        if (
            x > btnx
            and x < (btnx + btn_size_x)
            and y > btny
            and y < (btny + btn_size_y)
        ):
            print("ignore button save click")
            return

        print("add to list")
        click = MyClick(x, y, button, pressed)
        self.add_action(click)
        self.position_str = f"Click [{str(x).rjust(4)},{str(y).rjust(4)}]"

    def tk_on_click_save(self):
        self.write_to_file()
        print("Save")

    def tk_on_click_play(self):
        self.playing = True
        print("Play")
        self.read_macro()
        self.play_macro()

    def tk_on_click_clear(self):
        self.actions_list = []
        self.position_str = ""
        self.no_steps = 0
        print("Clear Macro")

    def tk_on_click_load(self):
        filename = fd.askopenfilename()
        print(filename)
        if filename is not None:
            self.macro_filename = filename
        else:
            print("no file selected")

        self.read_macro()
  

    def add_action(self, action: ActionUI):
        self.inc_steps()
        action.step_no = self.no_steps
        # needs to be dict to be saved later as json
        self.actions_list.append(action.to_dict())

    def write_to_file(self):
        with open("teste.json", "w") as f:
            json_file = dict(steps=self.actions_list)
            f.write(json.dumps(json_file))
            f.write("\n")

    def read_macro(self):
        if self.macro_filename is None and len(self.actions_list) > 0:
            self.actions_list = self.actions_list_from(dict(steps=self.actions_list))
            return
        else:
            showerror(title="No file selected yet.", message="File not Loaded.")

        with open(self.macro_filename, "r") as f:
            self.macro = json.loads(f.read())
        self.actions_list = self.actions_list_from(self.macro)

        if self.playing:
            return
        # populate listbox
        for a in self.actions_list:
            position_str = f"Click [{str(a.x).rjust(4)},{str(a.y).rjust(4)}]"
            listbox_widget.insert(tk.END, position_str)

    def play_macro(self):
        self.record = False
        action_gui = Action()
        while self.playing:
            if self.cnt > self.iterations:
                break
            for a in self.actions_list:
                print(f"step: {a.step_no}")
                action_gui.go_click(a.x, a.y, self.speed, pyautogui.easeInBack)
            self.cnt += 1
            print(f"macro cnt {self.cnt}/{self.iterations}")
        time.sleep(0.5)
        self.playing = False
        self.reset_cnt()  # reset
        showinfo(title="Macro", message="Finished!")

    def actions_list_from(self, param: dict) -> List[ActionUI]:
        actions = []
        for step in param["steps"]:
            en = None

            match step["button"]:
                case "left":
                    en = mouse.Button.left
                case "middle":
                    en = mouse.Button.middle
                case "right":
                    en = mouse.Button.right

            click = MyClick(step["x"], step["y"], mouse.Button(en), step["is_pressed"])
            click.step_no = step["step_no"]
            actions.append(click)
        return actions

    def set_record_ON(self):
        self.record = True
        print("Record On")

    def set_record_OFF(self):
        self.record = False


def update_gui():
    if len(action_ui.actions_list) == 0:
        listbox_widget.delete(0, tk.END)

    if action_ui.position_str != "" and action_ui.record:
        listbox_widget.insert(tk.END, action_ui.position_str)
    action_ui.position_str = ""
    root.after(100, update_gui)


if __name__ == "__main__":
    root = tk.Tk(className="JXTECH")
    root.resizable(False, False)

    root.geometry("400x245")
    action_ui = ActionForm()
    
    my_notebook= ttk.Notebook(root)
    my_notebook.pack(expand=1,fill=BOTH)
    #Create Tabs
    macro_tab= ttk.Frame(my_notebook)
    my_notebook.add(macro_tab, text= "Macro")
    
    tab2= ttk.Frame(my_notebook)
    my_notebook.add(tab2, text= "Settings")
    
    # panel
    top_pane = tk.PanedWindow(macro_tab, background="#99fb99")
    main = tk.PanedWindow(macro_tab, background="#99fb99")
    bottom_pane = tk.PanedWindow(macro_tab, background="#cccb99")

    listbox_entries = []
    scrollbar = Scrollbar(macro_tab)
    listbox_widget = Listbox(macro_tab, yscrollcommand=scrollbar.set)
    listbox_widget.pack(side="top", fill="x")
    top_pane.add(listbox_widget)

    bottom_pane.columnconfigure(0, weight=3)
    bottom_pane.columnconfigure(1, weight=2)
    bottom_pane.columnconfigure(2, weight=2)
    bottom_pane.columnconfigure(3, weight=2)
    bottom_pane.columnconfigure(4, weight=2)

    # BTN SAVE
    btn_save = ttk.Button(macro_tab, text="Save Macro", command=action_ui.tk_on_click_save)
    btn_save.grid(
        column=0,
        row=1,
        sticky=tk.S,
    )
    # bind is when you want to select a specific listener like the left or right mouse button
    # btn_save.bind("<Button-1>", action_ui.tk_on_click_save)
    action_ui.btn_save = btn_save
    # PLAY
    btn_play = ttk.Button(macro_tab, text="Play Macro", command=action_ui.tk_on_click_play)
    btn_play.grid(
        column=1,
        row=1,
        sticky=tk.S,
    )
    btn_load_macro = ttk.Button(
        macro_tab, text="Load Macro", command=action_ui.tk_on_click_load
    )
    btn_load_macro.grid(
        column=2,
        row=1,
        sticky=tk.S,
    )
    rec_image = PhotoImage(file=parse_path("./src/assets/record.png"))
    btn_record = ttk.Button(
        macro_tab, text="Rec", command=lambda: action_ui.set_record_ON(), image=rec_image
    )
    btn_record.grid(
        column=3,
        row=1,
        sticky=tk.S,
    )

    btn_clear = ttk.Button(macro_tab, text="Clear", command=action_ui.tk_on_click_clear)
    btn_clear.grid(
        column=4,
        row=1,
        sticky=tk.S,
    )

    scrollbar.config(command=listbox_widget.yview)

    bottom_pane.add(btn_save)
    bottom_pane.add(btn_play)
    bottom_pane.add(btn_load_macro)
    bottom_pane.add(btn_record)
    bottom_pane.add(btn_clear)
    # add to main pane
    main.add(top_pane)
    main.add(bottom_pane)
    # add to assemble
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    top_pane.grid(row=0, column=0, sticky="ew")
    main.grid(row=1, column=0, sticky="nsew")

    keyboard_listener = keyboard.Listener(on_release=action_ui.on_release)
    keyboard_listener.start()
    mouse_listener = mouse.Listener(on_click=action_ui.on_click)
    mouse_listener.start()

    # Collect events until released
    update_gui()
    root.mainloop()
