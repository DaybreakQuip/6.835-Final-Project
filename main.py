from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from record import record_to_file
import os
import time
import threading
from tkinter import *
from winsound import *

from text_analysis import *
from gesture_sentiment_analysis import *
from mailer import *
from speaker import *
from PIL import ImageTk,Image
import json
from keras.models import model_from_json
from scipy.constants import lb
import google.protobuf
from speech_sentiment_analysis import *

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
motion_inform = [False]

# Must be included in settings:
forbidden = []
CAN_SEND_EMAIL = False
RECEIVER_EMAILS = [""]
#########################################


output_dic = {"AVG_SPEECH_RATE": 130., "SAID_ILLEGALS": [], "MOOD": {
    "angry": 0,
    "disgust": 0,
    "fear": 0,
    "sad": 0,
    "surprise": 0,
    "neutral": 0,
}}

bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
time.sleep(2)
camera = cv2.VideoCapture(0)
camera.set(10, 200)

gesture_model_filename = './VGG_cross_validated.h5'
sentiment_model_filename = "./sentiment_model.h5"
gesture_model, gesture_graph, gesture_session = init_keras_thread(gesture_model_filename)
sentiment_model, sentiment_graph, sentiment_session = init_keras_thread(sentiment_model_filename)

####### WIP Speech To Emotion ######
###################################

def get_text_feedback(audio_filename):
    sr_thread = threading.Thread(target=check_speech_rate,args=(audio_filename,desired_rate, output_dic))
    sr_thread.start()
    filler_thread = threading.Thread(target=check_filler_words,args=(audio_filename,forbidden, output_dic))
    filler_thread.start()

def get_gesture_feedback():
    gesture_thread = threading.Thread(target=analyze_gesture,args=(capture_image(camera, bgModel), \
        gesture_model, gesture_graph, gesture_session, output_dic))
    gesture_thread.start()

def get_motion_feedback():
    motion_inform[0] = True
    motion_thread = threading.Thread(target=capture_motion, args=(camera, motion_inform))
    motion_thread.start()

def get_sentiment_feedback():
    sentiment_thread = threading.Thread(target=analyze_sentiment,args=(capture_image(camera, bgModel, mode="sentiment"), \
        sentiment_model, sentiment_graph, sentiment_session, output_dic))
    sentiment_thread.start()

def get_speech_emotion_feedback(audio_filename):
    results = []
    speech_emote = threading.Thread(target=speech_emotion_recognition, args=(audio_filename,results))
    speech_emote.start()
    while len(results) == 0:
        pass
    print(results)

def record_thread():
    global counter
    runner2 = threading.currentThread()
    get_motion_feedback()
    while getattr(runner2, "do_run", True):
        record_to_file(tmp_prefix_name + str(counter))
        get_text_feedback(f"{tmp_prefix_name}{counter}") if live_feedback_on else None
        # get_gesture_feedback() if camera.isOpened() else None
        # get_sentiment_feedback() if camera.isOpened() else None
        # get_speech_emotion_feedback(tmp_prefix_name + str(counter)) doesn't work atm
        counter += 1
    switch.configure(text="Start", command=start_command, state=NORMAL, bg="#BBFAC7")
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()

def stop_thread():
    global counter
    global last_file_counter
    temp = counter
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
    motion_inform[0] = False
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
    settings_window.geometry("300x500""+{}+{}".format(positionRight + 50, positionDown + 100))

    words_label = Label(settings_window, text="Illegal Words Entry:", font=("Courier",10))
    e = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e.insert(END, ' '.join(forbidden))
    words_label.pack()
    e.pack()

    def update_words():
        search_param = e.get("1.0","end-1c")
        forbidden.clear()
        forbidden.extend(search_param.split())

    list_of_words = Button(settings_window, text='Update', height=2, width=20, command=update_words)
    list_of_words.pack()


    email_label = Label(settings_window, text="Send Report to Email?:", font=("Courier",10))
    email_option = Combobox(settings_window, values=["Send Report", "Don't Send Report"])
    email_label.pack()
    email_option.pack()

    address_label = Label(settings_window, text="Enter Email Addresses:", font=("Courier",10))
    e_address = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e_address.insert(END, ' '.join(RECEIVER_EMAILS))

    def update_address():
        search_param = e_address.get("1.0","end-1c")
        RECEIVER_EMAILS.clear()
        RECEIVER_EMAILS.extend(search_param.split())

    address_label.pack()
    address_update = Button(settings_window, text='Update', height=2, width=20, command=update_address)
    e_address.pack()
    address_update.pack()

    def email_option_selected(event):
        global CAN_SEND_EMAIL
        if email_option.get() == "Send Report":
            CAN_SEND_EMAIL = True
        else:
            CAN_SEND_EMAIL = False

    email_option.bind("<<ComboboxSelected>>", email_option_selected)


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
def fun_stuff_delete_later(event):
    play = lambda: PlaySound('ui_sample.wav', SND_FILENAME)
    a = threading.Thread(target=play)
    a.start()
image=ImageTk.PhotoImage(Image.open("abstract-image.jpg"))
background_label = Label(root, image=image, height=120, width=120)
background_label.bind("<Button>", fun_stuff_delete_later)

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

if CAN_SEND_EMAIL:
    send_message(compose_message(output_dic), RECEIVER_EMAILS)
