import threading
from tkinter import *
import time

runner1 = None
runner2 = None

def record_thread():
    runner2 = threading.currentThread()
    while getattr(runner2, "do_run", True):
        print("Hi, I am your first thread talking.")
        time.sleep(3)
    print("Stopping first thread")

def stop_thread():
    runner1 = threading.currentThread()
    while getattr(runner1, "do_run", True):
        print("Hi, I am your second thread talking.")
        time.sleep(3)
    print("Stopping second thread")

def start_command():
    global runner1
    global runner2
    runner1 = threading.Thread(target=record_thread,args=())
    runner1.start()
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()
    switch.configure(text="Stop", command=stop_command)

def stop_command():
    global runner1
    global runner2
    runner1.do_run = False
    runner2.do_run = False
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