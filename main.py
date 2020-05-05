from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from record import record_to_file
import os
import time
import threading
import wave
from datetime import datetime
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
from settings_ui import settings_win, setting_params

dir_path = os.path.dirname(os.path.realpath(__file__))

runner1 = None
counter = 0
last_file_counter = 0
tmp_prefix_name = "recording_"
state = False
time_count = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'
motion_inform = [False]

#########################################

desired_rate = 180 if setting_params["desired_rate_mode"] == "fast" else 150 # we will have two categories: slow or fast. slow -> 150, fast -> 180

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
def update_log(today_string):
    try:
        with open(setting_params["username"] + ".json", "r+") as f:
            logs = json.load(f)
            f.seek(0)
            f.truncate()
            logs[today_string] = output_dic
            json.dump(logs, f)
    except:
        with open(setting_params["username"] + ".json", "w+") as f:
            logs = {}
            logs[today_string] = output_dic
            json.dump(logs, f)

def get_text_feedback(audio_filename):
    sr_thread = threading.Thread(target=check_speech_rate,args=(audio_filename,desired_rate, output_dic, setting_params["live_feedback_on"], setting_params["voice_on"], root))
    sr_thread.start()
    filler_thread = threading.Thread(target=check_filler_words,args=(audio_filename,setting_params["forbidden"], output_dic, setting_params["live_feedback_on"],setting_params["voice_on"], root))
    filler_thread.start()

def get_gesture_feedback():
    gesture_thread = threading.Thread(target=analyze_gesture,args=(capture_image(camera, bgModel), \
        gesture_model, gesture_graph, gesture_session, output_dic, setting_params["live_feedback_on"]))
    gesture_thread.start()

def get_motion_feedback():
    motion_inform[0] = True
    motion_thread = threading.Thread(target=capture_motion, args=(camera, motion_inform, setting_params["live_feedback_on"], setting_params["voice_on"], root))
    motion_thread.start()

def get_sentiment_feedback():
    sentiment_thread = threading.Thread(target=analyze_sentiment,args=(capture_image(camera, bgModel, mode="sentiment"), \
        sentiment_model, sentiment_graph, sentiment_session, output_dic, setting_params["live_feedback_on"]))
    sentiment_thread.start()

def get_speech_emotion_feedback(audio_filename):
    results = []
    speech_emote = threading.Thread(target=speech_emotion_recognition, args=(audio_filename,results, setting_params["live_feedback_on"]))
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
        get_text_feedback(f"{tmp_prefix_name}{counter}") if setting_params["live_feedback_on"] else None
        # get_gesture_feedback() if camera.isOpened() and setting_params["live_feedback_on else None
        # get_sentiment_feedback() if camera.isOpened() and setting_params["live_feedback_on else None
        # get_speech_emotion_feedback(tmp_prefix_name + str(counter)) if camera.isOpened() and setting_params["live_feedback_on else None
        counter += 1
    switch.configure(text="Start", command=start_command, state=NORMAL, bg="#BBFAC7")
    runner2 = threading.Thread(target=stop_thread,args=())
    runner2.start()

def stop_thread():
    global counter
    global last_file_counter
    time.sleep(6)
    temp = counter

    # combine all tmp sound files into summary.wav file and delete tmp files
    outfile = "summary.wav"
    set_params = False
    output = wave.open(outfile, 'wb')
    for i in range(last_file_counter, counter):
        infile = f"{tmp_prefix_name}" + str(i) + ".wav"
        textgrid_file = f"{tmp_prefix_name}" + str(i) + ".TextGrid"
        w = wave.open(infile, 'rb')
        if not set_params:
            output.setparams(w.getparams())
            set_params = True
        output.writeframes(w.readframes(w.getnframes()))
        w.close()
        try:
            os.remove(dir_path + "\\" + infile)
            os.remove(dir_path + "\\" + textgrid_file)
        except Exception as e:
            print(e)
            print("Unable to find/delete certain tmp files")
            continue

    output.close()

    ##############

    get_text_feedback("summary.wav") if not setting_params["live_feedback_on"] else None

    today_string = str(datetime.now())
    update_log(today_string) if setting_params["username"] != "" else None

    last_file_counter = temp

    if setting_params["CAN_SEND_EMAIL"]:
        send_message(compose_message(output_dic), setting_params["RECEIVER_EMAILS"])

    if setting_params["GET_SUMMARY"] and setting_params["username"] != "":
        with open(setting_params["username"] + ".json", "r") as f:
            logs = json.load(f)
            compose_summary(logs)

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
switch = Button(root, text='Start', height=2, width= 20, command=start_command, bg="#BBFAC7",font=("Courier", 10))
settings = Button(root, text='Settings', height=2, width=30, bg="#AEAEAE",command= lambda: settings_win(root, positionRight, positionDown),font=("Courier", 10))

background_label.pack()
title.pack(side=TOP, pady = 100)
timer.pack(side=TOP, pady= 10)
settings.pack(side=BOTTOM, pady=5)
switch.pack(side=BOTTOM, pady=5)

update_timer()
mainloop()
