import threading
from tkinter import *
import time
from record import *
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

runner1 = None
counter = 0
last_file_counter = 0
def record_thread():
    global counter
    runner2 = threading.currentThread()
    while getattr(runner2, "do_run", True):
        record_to_file("recording_" + str(counter))
        counter += 1
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()

def stop_thread():
    global counter
    global last_file_counter
    temp = counter
    runner1 = threading.currentThread()
    for i in range(last_file_counter, counter):
        os.remove(dir_path + "\\recording_" + str(i) + ".wav")
    last_file_counter = temp
    print("stopped deleting")

def start_command():
    global runner1
    runner1 = threading.Thread(target=record_thread,args=())
    runner1.start()
    switch.configure(text="Stop", command=stop_command)

def stop_command():
    global runner1
    runner1.do_run = False
    switch.configure(text="Start", command=start_command)

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