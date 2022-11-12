from time import time
import pyautogui
from pyautogui import alert, sleep
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import Label, Button, StringVar
from classes.interval import Interval
from classes.smithing import Smithing
from playsound import playsound

root = tk.Tk(className='escape from boredom - v01')
root.geometry("200x200")

button = tk.Button(root, text="I am a button")

smithing = Smithing("Smithing", forge=[1939, 370], anvil=[1770, 548])
smithing.set_MAX_ITERATIONS(9)
INTERVAL_TIME = 35


def has_found_img(pos):
    if pos[0] != -1:
        return True
    else:
        return False


def set_next_cycle():
    time_to_act = datetime.now() + timedelta(0, INTERVAL_TIME)
    smithing.set_time_to_act(time_to_act)


def show_next_cycle():
    dt_diff = smithing.get_time_to_act() - datetime.now()
    app_status.set(f'Next cycle in: {dt_diff.seconds}s')


@Interval(interval=INTERVAL_TIME)
def main_loop():
    if smithing.forge_found or smithing.forge != None:

        # HEAT BAR
        pos = smithing.find_image("./assets/colled_bar.png")
        if pos is not None:
            # click forge
            Smithing.go_click(
                smithing.forge[0], smithing.forge[1], 2, pyautogui.easeInBack)
            sleep(3)
            print(f'cold bar not found {pos}')
        else:
            print(f'cold bar not found')
            return

        # click forge
        Smithing.go_click(
            smithing.forge[0], smithing.forge[1], 2, pyautogui.easeInBack)
        # Click runeplate
        pos = smithing.find_image("./assets/sm_rune_plate.png")
        if pos is not None:
            Smithing.go_click(pos[0]+20, pos[1]+22, 2, pyautogui.easeInElastic)
        else:
           print(f'Not found menu.')

        # begin project
        pos = smithing.find_image("./assets/begin_project.png")
        if pos is not None:
            Smithing.go_click(pos[0]+20, pos[1]+20, 2, pyautogui.easeInElastic)
            sleep(3)
        else:
            print(f'Begin project btn not found')

        # click anvil
        pos = smithing.find_image("./assets/anvil.png")
        if pos is None:
            pos = smithing.anvil
        if pos is not None:
            Smithing.go_click(pos[0], pos[1], 2, pyautogui.easeInElastic)
        else:
            app_status.set(f'Image Not found')
            print("Image Not found.")
        # wait to cool down
        sleep(30)
        smithing.add_iterations(1)
    else:
        msg.set(f"Can't proceed without a orebox !")
        smithing.set_iterations(9)
        playsound('./assets/456962__funwithsound__failure-drum-sound-effect-1.mp3')
    set_next_cycle()


def smith(cycles=9):
    set_next_cycle()
    smithing.find_and_set_forge()
    smithing.find_and_set_anvil()
    txt_ore_box.set(
        f"Has found ore box|anvil ? {smithing.forge_found}|{smithing.anvil_found}")
    smithing.set_MAX_ITERATIONS(cycles)
    while smithing.get_iterations() < smithing.get_MAX_ITERATIONS():
        main_loop()
        msg.set(
            f'Status: Running...\n Nº iterations {smithing.get_iterations()}')
        show_next_cycle()
        root.update()
        sleep(1)
    app_status.set(f'Script ended.')


if __name__ == "__main__":
    # playsound('./assets/391539__mativve__electro-win-sound.wav')
    start_button2 = Button(root, text="start smithing",
                           command=lambda: smith(9))
    start_button2.pack()
    msg = StringVar()
    msg.set(f'Script started.')

    app_status = StringVar()
    app_status.set(f'All nominal.')
    app_status.set(f'Interval time set to: {INTERVAL_TIME}s')

    txt_ore_box = StringVar()
    txt_ore_box.set(
        f"Has found ore box|anvil ? {smithing.forge_found}|{smithing.anvil_found}")

    label = Label(root, textvariable=msg)
    label.pack()

    lbl_ore_box = Label(root, textvariable=txt_ore_box)
    lbl_ore_box.pack()

    lbl_app_status = Label(root, textvariable=app_status)
    lbl_app_status.pack()
    root.mainloop()
    alert(text='Finished...', title='Smithing', button='OK')
