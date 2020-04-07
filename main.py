from record import record_to_file
import os
import time
import tkinter

from text_analysis import *
from gesture_analysis import *
from speaker import *
from utils import *
import os

COUNTER = 0

def run_GUI():
    pass 


def main():
    load_speech("6UAssist is starting...")
    unload_speech()

    run_GUI()
    clean_tmps()

    load_speech("Thank you for using 6UAssist")
    unload_speech()
    # os.remove(DATA_FILENAME) # remove data file of user

if __name__ == '__main__':
    print("6UAssist is starting...")
    main()
    print("Thank you for using 6UAssist")
