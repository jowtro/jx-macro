from pyautogui import sleep
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import Label, Button, StringVar
from classes.interval import Interval
from classes.mining import Mining
from playsound import playsound
from pynput import keyboard
root = tk.Tk(className='escape from boredom - v01')
root.geometry("200x200")

button = tk.Button(root, text="I am a button")
mark_to_exit = False
# janela dividida
mining = Mining("Mining", rock=[1803, 469])
# portatil
# mining = Mining("Mining", rock=[ 812, 436])
INTERVAL_TIME = 25


def has_found_img(pos):
    if pos[0] != -1:
        return True
    else:
        return False


def on_release(key):
    global mark_to_exit
    if key == keyboard.Key.esc:
        mark_to_exit = True
        playsound('./assets/456962__funwithsound__failure-drum-sound-effect-1.mp3')


def set_next_cycle():
    time_to_act = datetime.now() + timedelta(0, INTERVAL_TIME)
    mining.set_time_to_act(time_to_act)


def show_next_cycle():
    dt_diff = mining.get_time_to_act() - datetime.now()
    app_status.set(f'Next cycle in: {dt_diff.seconds}s')


@Interval(interval=INTERVAL_TIME)
def main_loop():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()

    if mining.metal_box_found:
        mining.mine()
        mining.add_iterations(1)
    else:
        msg.set("Can't proceed without a orebox !")
        mining.set_iterations(9)
        playsound('./assets/456962__funwithsound__failure-drum-sound-effect-1.mp3')
    set_next_cycle()


def mine(cycles=9):
    global mark_to_exit
    mark_to_exit = False
    set_next_cycle()
    mining.set_iterations(0)
    mining.set_MAX_ITERATIONS(cycles)
    lbl_elapsed = datetime.now()
    while mining.get_iterations() < mining.get_MAX_ITERATIONS() and not mark_to_exit:
        main_loop()
        msg.set(
            f'Status: Running...\n Nº iterations {mining.get_iterations()}')
        show_next_cycle()
        loop_date = datetime.now()
        diff_Dt = loop_date - lbl_elapsed
        app_elapsed.set(f'Elapsed time: {str(diff_Dt)[:10]}')
        root.update()
        sleep(1)
    app_status.set('Script ended.')


if __name__ == "__main__":
    playsound('./assets/391539__mativve__electro-win-sound.wav')
    mining.find_and_set_orebox()
    start_button = Button(root, text="Mine Runite", command=lambda: mine(50))
    start_button.pack()
    start_button2 = Button(root, text="Mine lower ores",
                           command=lambda: mine(25))
    start_button2.pack()
    msg = StringVar()
    msg.set('Script started.')

    app_status = StringVar()
    app_status.set('All nominal.')
    app_status.set(f'Interval time set to: {INTERVAL_TIME}s')

    app_elapsed = StringVar()
    app_elapsed.set('Elpapsed time: ?')

    txt_ore_box = StringVar()
    txt_ore_box.set(f"Has found ore box ? {mining.metal_box_found}")

    label = Label(root, textvariable=msg)
    label.pack()

    lbl_ore_box = Label(root, textvariable=txt_ore_box)
    lbl_ore_box.pack()

    lbl_elapsed = Label(root, textvariable=app_elapsed)
    lbl_elapsed.pack()

    lbl_app_status = Label(root, textvariable=app_status)
    lbl_app_status.pack()
    root.mainloop()
