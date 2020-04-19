from tkinter.scrolledtext import ScrolledText

from record import record_to_file
import os
import time
import threading
from tkinter import *

from text_analysis import *
from gesture_sentiment_analysis import *
from mailer import *
from speaker import *
from utils import *
from PIL import ImageTk,Image

dir_path = os.path.dirname(os.path.realpath(__file__))

runner1 = None
counter = 0
last_file_counter = 0
live_feedback_on = True
tmp_prefix_name = "recording_"
desired_rate = 150
state = False
time_count = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'
forbidden = []

bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
time.sleep(2)
camera = cv2.VideoCapture(0)
camera.set(10, 200)

gesture_model_filename = './VGG_cross_validated.h5'
sentiment_model_filename = "./sentiment_model.h5"
gesture_model, gesture_graph, gesture_session = init_keras_thread(gesture_model_filename)
sentiment_model, sentiment_graph, sentiment_session = init_keras_thread(sentiment_model_filename)

def get_live_feedback(filename, criteria={}):
    feedback_thread = threading.Thread(target=check_speech_rate,args=(filename,desired_rate))
    feedback_thread.start()

def get_gesture_feedback():
    gesture_thread = threading.Thread(target=analyze_gesture,args=(capture_image(camera, bgModel), \
        gesture_model, gesture_graph, gesture_session))
    gesture_thread.start()

def get_sentiment_feedback():
    sentiment_thread = threading.Thread(target=analyze_sentiment,args=(capture_image(camera, bgModel, mode="sentiment"), \
        sentiment_model, sentiment_graph, sentiment_session))
    sentiment_thread.start()

def record_thread():
    global counter
    runner2 = threading.currentThread()
    while getattr(runner2, "do_run", True):
        record_to_file(tmp_prefix_name + str(counter))
        get_live_feedback(f"{tmp_prefix_name}{counter}") if live_feedback_on else None
        # get_gesture_feedback() if camera.isOpened() else None
        # get_sentiment_feedback() if camera.isOpened() else None
        counter += 1
    switch.configure(text="Start", command=start_command, state=NORMAL, bg="#BBFAC7")
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()

def stop_thread():
    global counter
    global last_file_counter
    temp = counter
    #runner1 = threading.currentThread()
    for i in range(last_file_counter, counter):
        try:
            os.remove(dir_path + f"\\{tmp_prefix_name}" + str(i) + ".wav")
            os.remove(dir_path + f"\\{tmp_prefix_name}" + str(i) + ".TextGrid")
        except:
            print("Unable to find/delete certain tmp files")
    last_file_counter = temp
    
    if CAN_SEND_EMAIL:
        send_message(compose_message())

def start_command():
    global runner1
    global state
    state = True
    runner1 = threading.Thread(target=record_thread,args=())
    runner1.start()
    switch.configure(text="Stop", command=stop_command,bg="#FF7B5D")

def stop_command():
    global runner1
    global state
    global time_count
    state = False
    time_count = [0, 0, 0]
    timer.configure(text='00:00:00')
    runner1.do_run = False
    switch.config(text="Processing", state="disabled")
    try:
        os.remove(dir_path + "\\data.csv")
    except:
        print("Unable to delete summary.csv, most likely it doesn't exist.")

def update_timer():
    if state:
        global timer
        time_count[2] += 1
        if time_count[2] >= 100:
            time_count[2] = 0
            time_count[1] += 1
        if time_count[1] >= 60:
            time_count[0] += 1
            time_count[1] = 0
        timer.config(text=pattern.format(time_count[0],time_count[1],time_count[2]))
    root.after(10, update_timer)

def settings_win():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("200x300""+{}+{}".format(positionRight + 50, positionDown + 100))

    words_label = Label(settings_window, text="Illegal Words Entry:", font=("Courier",10))
    e = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e.insert(END, ' '.join(forbidden))
    words_label.pack()
    e.pack()

    def update_words():
        search_param = e.get("1.0","end-1c")
        forbidden.clear()
        forbidden.extend(search_param.split())
        print(forbidden)

    list_of_words = Button(settings_window, text='Update', height=2, width=20, command=update_words)
    list_of_words.pack()


    settings_window.transient(root)
    settings_window.grab_set()
    root.wait_window(settings_window)


root = Tk()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2) - 60
positionDown = int(root.winfo_screenheight()/4 - windowHeight/4) - 50

root.geometry("300x600""+{}+{}".format(positionRight, positionDown))
title = Label(root, text="6.UAssist")
timer = Label(root, text="00:00:00", font=("Courier", 35))

image=ImageTk.PhotoImage(Image.open("best.png"))
background_label = Label(root, image=image, height=120, width=120)



title.config(font=("Courier", 35))
switch = Button(root, text='Start', height=2, width= 20, command=start_command, bg="#BBFAC7")
settings = Button(root, text='Settings', height=2, width=30, bg="#AEAEAE",command=settings_win)

background_label.pack()
title.pack(side=TOP, pady = 100)
timer.pack(side=TOP, pady= 10)
settings.pack(side=BOTTOM, pady=5)
switch.pack(side=BOTTOM, pady=5)

update_timer()
mainloop()