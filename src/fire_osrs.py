from classes.fire import Fire
from classes.interval import Interval
from playsound import playsound
from helper.file_helper import parse_path

action = Fire("Firemaking")
action.set_MAX_ITERATIONS(15)
INTERVAL_TIME = 1


def has_found_img(pos):
    if pos[0] != -1:
        return True
    else:
        return False


@Interval(interval=INTERVAL_TIME)
def main_loop():
    action.burn_log()


def start():
    while action.get_iterations() < action.get_MAX_ITERATIONS():
        main_loop()


if __name__ == "__main__":
    #playsound(parse_path("./src/assets/ok.wav"))
    start()
