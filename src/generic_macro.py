from time import time
import pyautogui
from pyautogui import alert, sleep
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import Label, Button, StringVar
from classes.interval import Interval
from classes.fishing import Fishing
from playsound import playsound

action = Fishing("Fishing")
action.set_MAX_ITERATIONS(9)
INTERVAL_TIME = 5


def has_found_img(pos):
    if pos[0] != -1:
        return True
    else:
        return False

@Interval(interval=INTERVAL_TIME)
def main_loop():
    
    sleep(2)


def action(cycles=9):
    action.set_MAX_ITERATIONS(cycles)
    while action.get_iterations() < action.get_MAX_ITERATIONS():
        main_loop()
        sleep(1)


if __name__ == "__main__":
    playsound('./assets/391539__mativve__electro-win-sound.wav')

