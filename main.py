from record import record_to_file
import os
import time
import threading
from tkinter import *

from text_analysis import *
from gesture_analysis import *
from speaker import *
from utils import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

runner1 = None
counter = 0
last_file_counter = 0
live_feedback_on = True
tmp_prefix_name = "recording_"
desired_rate = 150

def get_live_feedback(filename, criteria={}):
    check_speech_rate(filename, desired_rate)
    
def record_thread():
    global counter
    runner2 = threading.currentThread()
    while getattr(runner2, "do_run", True):
        record_to_file(tmp_prefix_name + str(counter))
        get_live_feedback(f"{tmp_prefix_name}{counter}") if live_feedback_on else None
        counter += 1
    switch.configure(text="Start", command=start_command, state=NORMAL)
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()

def stop_thread():
    global counter
    global last_file_counter
    temp = counter
    runner1 = threading.currentThread()
    for i in range(last_file_counter, counter):
        try:
            os.remove(dir_path + f"\\{tmp_prefix_name}" + str(i) + ".wav")
            os.remove(dir_path + f"\\{tmp_prefix_name}" + str(i) + ".TextGrid")
        except:
            print("Unable to find/delete certain tmp files")
    last_file_counter = temp

def start_command():
    global runner1
    runner1 = threading.Thread(target=record_thread,args=())
    runner1.start()
    switch.configure(text="Stop", command=stop_command)

def stop_command():
    global runner1
    runner1.do_run = False
    switch.config(text="Processing", state="disabled")
    try:
        os.remove(dir_path + "\\data.csv")
    except:
        print("Unable to delete summary.csv, most likely it doesn't exist.")


root = Tk()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2) - 60
positionDown = int(root.winfo_screenheight()/4 - windowHeight/4) - 50

root.geometry("300x600""+{}+{}".format(positionRight, positionDown))
switch = Button(root, text='Start', height=2, width= 20, command=start_command)
settings = Button(root, text='Settings', height=2, width=30)
settings.pack(side=BOTTOM, pady=5)
switch.pack(side=BOTTOM, pady=5)

mainloop()