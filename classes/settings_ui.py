import tkinter
from helper.file_helper import parse_path
import toml

from util.util import get_setting


class SettingsUI:
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
        self.load_settings()

    def load_settings(self):
        try:
            with open(parse_path("./settings.toml"), "r") as f:
                self.conf = toml.load(f)
                if self.conf  is not None and self.conf :
                    self.iterations = get_setting("iterations", self.conf["settings"])
                    self.speed = get_setting("speed", self.conf["settings"])
                else:
                    self.conf = dict(settings={"iterations": 2, "speed": 2})
        except IOError as ex:
            ex.add_note("Can't read settings file")
            print(ex)
            tkinter.messagebox.showerror(title="Error", message=str(ex))

    def tk_save_settings(self):
        try:
            self.conf["settings"]["iterations"] = int(self.txt_iter.get())
            self.conf["settings"]["speed"] = float(self.txt_speed.get())
            with open(parse_path("./settings.toml"), "w") as f:
                toml.dump(self.conf, f)
            tkinter.messagebox.showinfo(title="Info", message="Settings Saved!")

        except IOError as ex:
            ex.add_note("Can't write settings file")
            tkinter.messagebox.showerror(title="Error", message=str(ex))
