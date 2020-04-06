from record import record_to_file
import os
import time
import tkinter

from analysis import *
from speaker import *
from utils import *

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

if __name__ == '__main__':
    print("6UAssist is starting...")
    main()
    print("Thank you for using 6UAssist")
