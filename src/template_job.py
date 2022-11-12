from classes.fire import Fire
from classes.interval import Interval
from playsound import playsound

action = Fire("Firemaking")
action.set_MAX_ITERATIONS(9)
INTERVAL_TIME = 0.2


def has_found_img(pos):
    if pos[0] != -1:
        return True
    else:
        return False

@Interval(interval=INTERVAL_TIME)
def main_loop():
    action.burn_log()


def start(cycles=9):
    action.set_MAX_ITERATIONS(cycles)
    while action.get_iterations() < action.get_MAX_ITERATIONS():
        main_loop()


if __name__ == "__main__":
    playsound('./assets/391539__mativve__electro-win-sound.wav')
    start()
