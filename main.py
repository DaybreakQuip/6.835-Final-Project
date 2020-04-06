from record import record_to_file
import os
import time

from analysis import *
from speaker import *
from utils import *

COUNTER = 0

def main():
    load_speech("hi world")
    unload_speech()

if __name__ == '__main__':
    print("6UAssist is starting...")
    main()
    clean_tmps()
    print("Thank you for using 6UAssist")
