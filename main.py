from analysis import *
from speaker import *
from record import record_to_file
import os
import time

COUNTER = 0

def main():
    load_speech("hi world")
    unload_speech()

if __name__ == '__main__':
    print("6UAssist is starting...")
    main()
    print("Thank you for using 6UAssist")
