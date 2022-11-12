from time import time
import pyautogui
from pyautogui import alert, sleep
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import Label, Button, StringVar
from classes.interval import Interval
from classes.smithing import Smithing
from playsound import playsound
from pynput import keyboard

root = tk.Tk(className='escape from boredom - v01')
root.geometry("200x200")

button = tk.Button(root, text="I am a button")

# Tela dividida
# smithing = Smithing("Smithing", forge=[970, 379], anvil=[862, 529])
# tela
smithing = Smithing("Smithing", forge=[1939, 370], anvil=[1770, 548])
smithing.set_MAX_ITERATIONS(9)
INTERVAL_TIME = 5
mark_to_exit = False


def on_release(key):
    global mark_to_exit
    if key == keyboard.Key.esc:
        mark_to_exit = True
        playsound('./assets/456962__funwithsound__failure-drum-sound-effect-1.mp3')


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
    listener = keyboard.Listener(on_release=on_release)
    listener.start()

    if smithing.forge_found or smithing.forge is not None:

        # click forge
        Smithing.go_right_click(
            smithing.forge[0], smithing.forge[1], 0.3, pyautogui.easeInOutBack)
        Smithing.go_click(
            smithing.forge[0], smithing.forge[1]+72, 0.3, pyautogui.easeInSine)
        sleep(2)
        # begin project
        pos = smithing.find_image("./assets/begin_project.png")
        if pos is not None:
            Smithing.go_click(pos[0]+20, pos[1]+20, 0.3, pyautogui.easeInSine)
        else:
            print('Begin project btn not found')

        # click anvil
        # pos = smithing.find_image("./assets/anvil.png")
        # if pos is None:
        #     pos = smithing.anvil
        # if pos is not None:
        #     Smithing.go_click(pos[0], pos[1], 2, pyautogui.easeInElastic)
        # else:
        #     app_status.set(f'Image Not found')
        #     print("Image Not found.")
        # wait to cool down
        sleep(1)
        smithing.add_iterations(1)
    else:
        msg.set("Can't proceed without a orebox !")
        smithing.set_iterations(9)
        playsound('./assets/456962__funwithsound__failure-drum-sound-effect-1.mp3')
    set_next_cycle()


def smith(cycles=9):
    global mark_to_exit
    set_next_cycle()
    mark_to_exit = False
    smithing.find_and_set_forge()
    smithing.find_and_set_anvil()
    txt_ore_box.set(
        f"Has found ore box|anvil ? {smithing.forge_found}|{smithing.anvil_found}")
    smithing.set_MAX_ITERATIONS(cycles)
    lbl_elapsed = datetime.now()
    while smithing.get_iterations() < smithing.get_MAX_ITERATIONS() and not mark_to_exit:
        msg.set(
            f'Status: Running...\n Nº iterations {smithing.get_iterations()}')
        main_loop()
        show_next_cycle()
        loop_date = datetime.now()
        diff_Dt = loop_date - lbl_elapsed
        app_elapsed.set(f'Elapsed time: {str(diff_Dt)[:9]}')
        root.update()
        sleep(1)
    app_status.set('Script ended.')


if __name__ == "__main__":
    # playsound('./assets/391539__mativve__electro-win-sound.wav')
    start_button2 = Button(root, text="start smithing arrows",
                           command=lambda: smith(23))
    start_button2.pack()
    msg = StringVar()
    msg.set('Script started.')

    app_status = StringVar()
    app_status.set('All nominal.')
    app_status.set(f'Interval time set to: {INTERVAL_TIME}s')

    app_elapsed = StringVar()
    app_elapsed.set('Elpapsed time: ?')

    txt_ore_box = StringVar()
    txt_ore_box.set(
        f"Has found ore box|anvil ? {smithing.forge_found}|{smithing.anvil_found}")

    label = Label(root, textvariable=msg)
    label.pack()

    lbl_ore_box = Label(root, textvariable=txt_ore_box)
    lbl_ore_box.pack()

    lbl_app_status = Label(root, textvariable=app_status)
    lbl_app_status.pack()

    lbl_elapsed = Label(root, textvariable=app_elapsed)
    lbl_elapsed.pack()

    root.mainloop()
