import json
import os
from pathlib import Path
import time
import tkinter as tk
from tkinter import BOTH, END, WORD, Image, PhotoImage
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import simpledialog
from tkinter import tix
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText
from tkinter.tix import Balloon
from tkinter.tix import Tk
from PIL import Image, ImageTk
from typing import List

import pyautogui
from pynput import keyboard, mouse
from classes.ac_screenshot import AcScreenshot
from classes.ac_screenshot_all import AcScreenshotAll
from classes.ac_wait import AcWait

from classes.action import Action
from classes.action_ui import ActionUI
from classes.my_click import MyClick
from classes.settings_ui import SettingsUI
from helper.file_helper import parse_path
from mapper.action_map import ActionMap
from util.util import set_txt_status


class ActionForm(SettingsUI):
    def __init__(self) -> None:
        super().__init__()
        self.root = Tk(className="JXTECH")
        self.root.resizable(False, False)
        self.image_file_extensions = {".jpg", ".png"}
        if os.name == "nt":
            self.root.geometry("525x245")
        else:
            self.root.geometry("590x255")
        self.my_filetypes = [("png format", ".png"), ("jpeg format", ".jpg")]
        self.my_filetypes2 = [("JSON format", ".json")]
        self.img_stop_record = PhotoImage(file=parse_path("./assets/stop_record.png"))
        self.img_record = PhotoImage(file=parse_path("./assets/record.png"))
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

        settings_tab = ttk.Frame(my_notebook)
        my_notebook.add(settings_tab, text="Settings")
        
        # Settings Tab
        settings_panel = tk.PanedWindow(settings_tab, background="#CCCCCC")
        settings_btn_panel = tk.PanedWindow(settings_tab, background="#CCCCCC")
        settings_tab.grid_rowconfigure(2, weight=1)
        settings_tab.grid_columnconfigure(2, weight=1)
        settings_panel.grid_rowconfigure(2, weight=1)
        settings_panel.grid_columnconfigure(2, weight=1)
        btn_save_settings = ttk.Button(
            settings_tab, text="Save Settings", command=self.tk_save_settings
        )
        btn_save_settings.grid(column=0, row=0, sticky=tk.S)
        self.lbl_ite = tk.Label(settings_panel, text="Iterations")
        self.txt_iter_val = tk.StringVar(value=self.conf["settings"]["iterations"])
        self.txt_iter = tk.Entry(settings_panel, textvariable=self.txt_iter_val)
        self.txt_speed_val = tk.StringVar(value=self.conf["settings"]["speed"])
        self.lbl_speed = tk.Label(settings_panel, text="Speed")
        self.txt_speed = tk.Entry(settings_panel, textvariable=self.txt_speed_val)
        self.lbl_speed.grid(column=0, row=1, sticky=tk.S)
        self.txt_speed.grid(column=1, row=1, sticky=tk.S)
        # end settings

        # panel
        top_pane = tk.PanedWindow(macro_tab, background="#99fb99")
        right_pane = tk.PanedWindow(macro_tab, background="#CCCCCC", orient="vertical")
        main = tk.PanedWindow(macro_tab, background="#99fb99")
        bottom_pane = tk.PanedWindow(macro_tab, background="#cccb99")

        self.text = ScrolledText(macro_tab, width=40, height=10, wrap=WORD)
        self.text.grid(row=2, column=0, padx=10, pady=10)
        self.text.image_filenames = []
        self.text.images = []

        self.txt_status = tk.Text(right_pane, wrap=WORD, width=10, height=3)
        self.txt_status.insert(
            tk.INSERT, 'tip: You can stop the macro by pressing "ESC" as well.'
        )
        # endregion

        # region buttons
        btn_wait = tk.Button(macro_tab, text="Wait", command=self.tk_add_wait)
        btn_find_img = tk.Button(
            macro_tab, text="Find image and Click", command=self.tk_add_screenshot
        )
        btn_find_img_loop = tk.Button(
            macro_tab,
            text="Find image and Click Loop",
            command=lambda: self.tk_add_screenshot(True),
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
        self.btn_record = ttk.Button(
            macro_tab,
            text="Rec",
            command=lambda: self.tk_on_click_record_toggle(),
            image=self.img_record,
        )
        self.btn_record.grid(
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
        # tip
        #Create a tooltip
        tip = Balloon(self.root)  
        #Bind the tooltip with button
        tip.bind_widget(btn_play,balloonmsg="To stop a running macro press ESC.")
        
        # SETTINGS PANEL
        settings_panel.add(self.lbl_ite)
        settings_panel.add(self.txt_iter)
        settings_panel.add(self.lbl_speed)
        settings_panel.add(self.txt_speed)
        # btn panel
        settings_btn_panel.add(btn_save_settings)
        # add widgets to the panes
        top_pane.add(self.text)

        right_pane.add(btn_wait)
        right_pane.add(btn_find_img)
        right_pane.add(btn_find_img_loop)
        right_pane.add(self.txt_status)
        top_pane.add(right_pane)

        bottom_pane.add(btn_save)
        bottom_pane.add(btn_play)
        bottom_pane.add(btn_load_macro)
        bottom_pane.add(self.btn_record)
        bottom_pane.add(btn_clear)

        # add to main pane
        main.add(top_pane)
        main.add(bottom_pane)
        # add to assemble
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        settings_panel.grid(row=0, column=0, sticky="nsew")
        settings_btn_panel.grid(row=1, column=0, sticky="sw")
        top_pane.grid(row=0, column=0, sticky="nsew")
        right_pane.grid(row=0, column=1, sticky="ne", padx=5, pady=5)
        main.grid(row=1, column=0, sticky="nsew")

        # INPUT LISTENERS
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
        set_txt_status(self, "STATUS: MACRO RUNNING.")
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

    def tk_add_screenshot(self, loop=False):
        file_dialog = fd.askopenfilename(
            parent=self.root,
            initialdir=os.getcwd(),
            title="Please select a file:",
            filetypes=self.my_filetypes,
        )
        if not file_dialog:
            return

        screenshot_file = Path(file_dialog)

        button = simpledialog.askstring(
            "Input",
            "Type which button to press when click on the picture left, right, middle.",
            parent=self.root,
            initialvalue="left",
        )

        while button != "left" != "right" != "middle":
            button = simpledialog.askstring(
                "Input",
                "Wrong button type one of the following: left, right or middle.",
                parent=self.root,
            )

        ac_ss = (
            AcScreenshot(str(screenshot_file), button)
            if not loop
            else AcScreenshotAll(str(screenshot_file), button)
        )
        self.add_action(ac_ss)

        # Add image to Scrolltext
        img = Image.open(screenshot_file).resize((64, 64), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.text.image_create(tk.INSERT, padx=5, pady=5, image=img)
        self.text.images.append(img)  # Keep a reference.
        self.text.insert(tk.INSERT, "\n")
        if screenshot_file.suffix in self.image_file_extensions:
            self.text.insert(tk.INSERT, screenshot_file.name + "\n")
            self.text.image_filenames.append(screenshot_file)

    def add_action(self, action: ActionUI):
        self.inc_steps()
        action.step_no = self.no_steps
        # needs to be dict to be saved later as json
        self.actions_list.append(action)
        # check if the ScrolledText it's empty
        if len(self.text.get("1.0", "end-1c")) == 0:
            self.text.insert(tk.INSERT, f"{str(action)}")
        else:
            self.text.insert(tk.INSERT, f"\n{str(action)}")

    def write_to_file(self):
        file = fd.asksaveasfilename(
            parent=self.root,
            initialdir=os.getcwd(),
            title="Save as",
            filetypes=self.my_filetypes2,
        )
        if file:  # user selected file
            with open(file, "w") as f:
                aux_ist = [x.to_dict() for x in self.actions_list]
                json_file = dict(steps=aux_ist)
                f.write(json.dumps(json_file))
        else:  # user cancel the file browser window
            print("No file chosen")

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
                # self.actions_list = [x for x in self.macro["steps"]]
                for x in self.macro["steps"]:
                    obj = ActionMap.map(x)
                    self.actions_list.append(obj)

                    if isinstance(obj, AcScreenshot):
                        img_path = Path(obj.ss_filepath)
                        img = Image.open(img_path).resize(
                            (64, 64), Image.Resampling.LANCZOS
                        )
                        img = ImageTk.PhotoImage(img)
                        self.text.image_create(tk.INSERT, padx=5, pady=5, image=img)
                        self.text.images.append(img)  # Keep a reference.
                        if img_path.suffix in self.image_file_extensions:
                            self.text.insert(tk.INSERT, img_path.name + "\n")
                            self.text.image_filenames.append(img_path)

                    self.text.insert(tk.INSERT, f"{str(obj)}\n")
        else:
            showerror(title="No file selected yet.", message="File not Loaded.")
            return

    def play_macro(self):
        self.record = False
        action_gui = Action(self)
        while self.playing:
            # after all iterations
            if self.cnt > self.conf["settings"]["iterations"]:
                break
            print(
                "macro cnt {}/{}".format(self.cnt, self.conf["settings"]["iterations"])
            )
            for a in self.actions_list:
                if not self.playing:
                    break
                if isinstance(a, AcScreenshot):
                    action_gui.find_image_click(
                        image_path=a.ss_filepath,
                        button=a.button,
                        time=self.conf["settings"]["speed"],
                    )
                if isinstance(a, AcScreenshotAll):
                    action_gui.find_image_click_all(
                        a.ss_filepath, a.button, self.conf["settings"]["speed"]
                    )
                if isinstance(a, MyClick):
                    action_gui.go_click(
                        a.x,
                        a.y,
                        self.conf["settings"]["speed"],
                        a.button,
                        pyautogui.easeInBack,
                    )
                if isinstance(a, AcWait):
                    action_gui.wait(a.wait)
                pyautogui.sleep(0.01)
            self.cnt += 1
        pyautogui.sleep(0.5)
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

    def tk_on_click_record_toggle(self):
        self.record = not self.record
        print(f"Record {self.record}")

    def set_record_OFF(self):
        self.record = False

    def update_gui(self):
        """
        self.text.insert(INSERT, image_file_path.name+'\n')
        self.text.image_create(INSERT, padx=5, pady=5, image=img)
        self.text.images.append(img)  # Keep a reference.
        self.text.insert(INSERT, '\n')
        """
        if self.record:
            self.btn_record.configure(image=self.img_stop_record)
            self.btn_record.image = self.img_stop_record
            set_txt_status(self, "STATUS: MACRO RECORDING.")
        else:
            self.btn_record.configure(image=self.img_record)
            self.btn_record.image = self.img_record
            set_txt_status(self, "STATUS: MACRO STOPPED.")

        if len(self.actions_list) == 0:
            # Clear current contents.
            self.text.delete("1.0", tk.END)

        # if self.action_str != "" and self.record:
        #    self.text.insert(tk.INSERT, self.action_str+"\n")

        self.action_str = ""
        self.root.after(300, self.update_gui)


if __name__ == "__main__":
    ActionForm()
