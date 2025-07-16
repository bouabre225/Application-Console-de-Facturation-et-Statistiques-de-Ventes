import time
import os

def effacer_console():
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')