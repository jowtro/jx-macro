import json
import os
from pathlib import Path
import time
import tkinter as tk
from tkinter import BOTH, END, WORD, Image, PhotoImage
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import simpledialog
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from typing import List

import pyautogui
from pynput import keyboard, mouse
from classes.ac_screenshot import AcScreenshot
from classes.ac_wait import AcWait

from classes.action import Action
from classes.action_ui import ActionUI
from classes.my_click import MyClick
from helper.file_helper import parse_path
from mapper.action_map import ActionMap


class ActionForm:
    def __init__(self) -> None:
        self.action_str = None
        self.actions_list = []
        self.no_steps = 0
        self.macro = None
        self.btn_save = None
        self.macro_filename = None
        self.record = False
        self.playing = False
        self.cnt = 1
        self.iterations = 2
        self.speed = 0.5
        self.root = tk.Tk(className="JXTECH")
        self.root.resizable(False, False)
        self.image_file_extensions = {'.jpg', '.png'}
        if os.name == "nt":
            self.root.geometry("520x245")
        else:
            self.root.geometry("635x255")

        self.create_widgets()
        self.update_gui()
        self.root.mainloop()

    def create_widgets(self):
        # region INIT
        my_notebook = ttk.Notebook(self.root)
        my_notebook.pack(expand=1, fill=BOTH)
        # Create Tabs
        macro_tab = ttk.Frame(my_notebook)
        my_notebook.add(macro_tab, text="Macro")

        tab2 = ttk.Frame(my_notebook)
        my_notebook.add(tab2, text="Settings")

        # panel
        top_pane = tk.PanedWindow(macro_tab, background="#99fb99")
        right_pane = tk.PanedWindow(macro_tab, background="#CCCCCC", orient="vertical")
        main = tk.PanedWindow(macro_tab, background="#99fb99")
        bottom_pane = tk.PanedWindow(macro_tab, background="#cccb99")

        self.text = ScrolledText(macro_tab, width=40, height=10, wrap=WORD)
        self.text.grid(row=2, column=0, padx=10, pady=10)
        self.text.image_filenames = []
        self.text.images = []

        lbl_speed = tk.Label(macro_tab, text="Cursor speed")
        current_value = tk.StringVar(value=0)
        spin_box = ttk.Spinbox(
            self.root, from_=0, to=30, textvariable=current_value, wrap=True
        )

        # endregion

        # region buttons
        btn_wait = tk.Button(macro_tab, text="Wait", command=self.tk_add_wait)
        btn_find_img = tk.Button(
            macro_tab, text="Find image and Click", command=self.tk_add_screenshot
        )
        # BTN SAVE
        btn_save = ttk.Button(
            macro_tab, text="Save Macro", command=self.tk_on_click_save
        )
        btn_save.grid(
            column=0,
            row=1,
            sticky=tk.S,
        )
        # bind is when you want to select a specific listener like the left or right mouse button
        # btn_save.bind("<Button-1>", action_ui.tk_on_click_save)
        self.btn_save = btn_save
        # PLAY
        btn_play = ttk.Button(
            macro_tab, text="Play Macro", command=self.tk_on_click_play
        )
        btn_play.grid(
            column=1,
            row=1,
            sticky=tk.S,
        )
        btn_load_macro = ttk.Button(
            macro_tab, text="Load Macro", command=self.tk_on_click_load
        )
        btn_load_macro.grid(
            column=2,
            row=1,
            sticky=tk.S,
        )
        self.rec_image = PhotoImage(file=parse_path("./assets/record.png"))
        btn_record = ttk.Button(
            macro_tab,
            text="Rec",
            command=lambda: self.set_record_ON(),
            image=self.rec_image,
        )
        btn_record.grid(
            column=3,
            row=1,
            sticky=tk.S,
        )

        btn_clear = ttk.Button(macro_tab, text="Clear", command=self.tk_on_click_clear)
        btn_clear.grid(
            column=4,
            row=1,
            sticky=tk.S,
        )
        # endregion

        # add widgets to the panes
        top_pane.add(self.text)

        right_pane.add(lbl_speed)
        right_pane.add(spin_box)
        right_pane.add(btn_wait)
        right_pane.add(btn_find_img)
        top_pane.add(right_pane)

        bottom_pane.add(btn_save)
        bottom_pane.add(btn_play)
        bottom_pane.add(btn_load_macro)
        bottom_pane.add(btn_record)
        bottom_pane.add(btn_clear)

        # add to main pane
        main.add(top_pane)
        main.add(bottom_pane)
        # add to assemble
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        top_pane.grid(row=0, column=0, sticky="nsew")
        right_pane.grid(row=0, column=1, sticky="ne", padx=5, pady=5)
        main.grid(row=1, column=0, sticky="nsew")

        keyboard_listener = keyboard.Listener(on_release=self.on_release)
        keyboard_listener.start()
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

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
        if not pressed:  # avoid on release
            return

        if not self.record:
            return
        wndx, wndy = self.root.winfo_rootx(), self.root.winfo_rooty()
        wnd_w = self.root.winfo_width()
        wnd_h = self.root.winfo_height()
        # IGNORE CLICK ON THE WHOLE TK WINDOW
        if x > wndx and x < (wndx + wnd_w) and y > wndy and y < (wndy + wnd_h):
            return

        print("add to list")
        click = MyClick(x, y, button, pressed)
        self.add_action(click)

    def tk_on_click_save(self):
        self.write_to_file()
        print("Save")

    def tk_on_click_play(self):
        self.playing = True
        print("Play")
        self.read_macro()
        self.play_macro()

    def tk_on_click_clear(self):
        self.text.delete("1.0", END)  # Clear current contents.
        self.text.images.clear()
        self.actions_list = []
        self.action_str = ""
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

    def tk_add_wait(self):
        secs = simpledialog.askstring(
            "Input", "How long the script will wait (seconds)?", parent=self.root
        )
        acwait = AcWait(secs)
        self.add_action(acwait)

    def tk_add_screenshot(self):
        my_filetypes = [("png format", ".png"), ("jpeg format", ".jpg")]
        screenshot_file = Path(
            fd.askopenfilename(
                parent=self.root,
                initialdir=os.getcwd(),
                title="Please select a file:",
                filetypes=my_filetypes,
            )
        )
        button = simpledialog.askstring(
            "Input",
            "Type which button to press when click on the picture left, right, middle.",
            parent=self.root,
        )

        while button != "left" != "right" != "middle":
            button = simpledialog.askstring(
                "Input",
                "Wrong button type one of the following: left, right or middle.",
                parent=self.root,
            )

        ac_ss = AcScreenshot(str(screenshot_file), button)
        self.add_action(ac_ss)
        
        # Add image to Scrolltext
        img = Image.open(screenshot_file).resize((64, 64), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.text.image_create(tk.INSERT, padx=5, pady=5, image=img)
        self.text.images.append(img)  # Keep a reference.
        self.text.insert(tk.INSERT, '\n')
        if screenshot_file.suffix in self.image_file_extensions:
            self.text.insert(tk.INSERT, screenshot_file.name+'\n')
            self.text.image_filenames.append(screenshot_file)

    def add_action(self, action: ActionUI):
        self.inc_steps()
        action.step_no = self.no_steps
        # needs to be dict to be saved later as json
        self.actions_list.append(action)
        self.text.insert(tk.INSERT, f"\n{str(action)}")

    def write_to_file(self):
        with open("teste.json", "w") as f:
            aux_ist = [x.to_dict() for x in self.actions_list]
            json_file = dict(steps=aux_ist)
            f.write(json.dumps(json_file))

    def read_macro(self):
        if self.playing:
            return

        if (self.macro_filename is None or self.macro_filename == "") and len(
            self.actions_list
        ) > 0:
            self.actions_list = self.actions_list_from(dict(steps=self.actions_list))
            return
        elif self.macro_filename != "" or self.macro_filename is not None:
            self.actions_list = []
            # READ
            with open(self.macro_filename, "r") as f:
                self.macro = json.loads(f.read())
                #self.actions_list = [x for x in self.macro["steps"]]
                for x in self.macro["steps"]:
                    obj = ActionMap.map(x)
                    self.actions_list.append(obj)
                    
                    if isinstance(obj, AcScreenshot):
                        img_path = Path(obj.ss_filepath)
                        img = Image.open(img_path).resize((64, 64), Image.Resampling.LANCZOS)
                        img = ImageTk.PhotoImage(img)
                        self.text.image_create(tk.INSERT, padx=5, pady=5, image=img)
                        self.text.images.append(img)  # Keep a reference.
                        if img_path.suffix in self.image_file_extensions:
                            self.text.insert(tk.INSERT, img_path.name+'\n')
                            self.text.image_filenames.append(img_path)
                            
                    self.text.insert(tk.INSERT, f"{str(obj)}\n")
        else:
            showerror(title="No file selected yet.", message="File not Loaded.")
            return

    def play_macro(self):
        self.record = False
        action_gui = Action()
        while self.playing:
            # after all iterations
            if self.cnt > self.iterations:
                break
            for a in self.actions_list:
                if isinstance(a, AcScreenshot):
                    action_gui.find_image_click(a.ss_filepath,a.button, self.speed, pyautogui.easeInBack)
                if isinstance(a, MyClick):
                    action_gui.go_click(a.x, a.y, self.speed, pyautogui.easeInBack)
                if isinstance(a, AcWait):
                    action_gui.wait(5)
                
            self.cnt += 1
            print(f"macro cnt {self.cnt}/{self.iterations}")
        time.sleep(0.5)
        self.playing = False
        self.reset_cnt()  # reset
        showinfo(title="Macro", message="Finished!")

    def actions_list_from(self, param: dict) -> List[ActionUI]:
        actions = []
        for step in param["steps"]:
            match step["button"]:
                case "left":
                    button = mouse.Button.left
                case "middle":
                    button = mouse.Button.middle
                case "right":
                    button = mouse.Button.right

            click = MyClick(step["x"], step["y"], button, step["is_pressed"])
            click.step_no = step["step_no"]
            actions.append(click)
        return actions

    def set_record_ON(self):
        self.record = True
        print("Record On")

    def set_record_OFF(self):
        self.record = False

    def update_gui(self):
        """
        self.text.insert(INSERT, image_file_path.name+'\n')
        self.text.image_create(INSERT, padx=5, pady=5, image=img)
        self.text.images.append(img)  # Keep a reference.
        self.text.insert(INSERT, '\n')
        """
        if len(self.actions_list) == 0:
            # Clear current contents.
            self.text.delete("1.0", tk.END)

        # if self.action_str != "" and self.record:
        #    self.text.insert(tk.INSERT, self.action_str+"\n")

        self.action_str = ""
        self.root.after(100, self.update_gui)


if __name__ == "__main__":
    ActionForm()
