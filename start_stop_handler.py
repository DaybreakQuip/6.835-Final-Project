import threading
import os
from settings_ui import *
import wave
from gesture_handler import *
from text_analysis import *
from record import record_to_file
from text_handler import *
from mailer import *
from datetime import datetime


recorder_thread = None
counter = 0
last_file_counter = 0
tmp_prefix_name = "recording_"
dir_path = os.path.dirname(os.path.realpath(__file__))
UI_open = [True]

def start_command(root, camera, switch, settings):
    global recorder_thread
    recorder_thread = threading.Thread(target=record_thread,args=(root, camera, switch, settings))
    recorder_thread.start()
    switch.configure(text="Stop", command=lambda:stop_command(switch,),bg="#FF7B5D")
    settings.configure(state="disabled")

def stop_command(switch):
    global recorder_thread
    recorder_thread.do_run = False
    motion_inform[0] = False
    switch.config(text="Processing", state="disabled")
    try:
        os.remove(dir_path + "\\data.csv")
    except:
        print("Unable to delete summary.csv, most likely it doesn't exist.")

def gesture_start_thread(root, camera, switch, settings):
    current = time.time()
    global recorder_thread
    affirmation = []
    while UI_open[0] and recorder_thread is None:
        affirmation.append(capture_motion_2(camera))
        if time.time() - current > 5:
            affirmation.clear()
            current = time.time()
        if affirmation.count(True) > 4:
            start_command(root, camera, switch, settings)
            return

def stop_word_check(audio_filename, switch):
    spoken_words = get_words(audio_filename)
    if spoken_words and len(spoken_words) > 0 and setting_params["stop_phrase"] in spoken_words:
        stop_command(switch)


def record_thread(root, camera, switch, settings):
    global counter
    global recorder_thread
    current_recorder_thread = threading.currentThread()
    get_motion_feedback(camera, root)
    while getattr(current_recorder_thread, "do_run", True):
        record_to_file(tmp_prefix_name + str(counter))
        get_text_feedback(f"{tmp_prefix_name}{counter}", root) if setting_params["live_feedback_on"] else None
        threading.Thread(target=stop_word_check, args=(f"{tmp_prefix_name}{counter}", switch)).start()
        # get_gesture_feedback(camera) if camera.isOpened() and setting_params["live_feedback_on else None
        counter += 1
    switch.configure(text="Start", command=lambda: start_command(root, camera, switch, settings), state=NORMAL, bg="#BBFAC7")
    settings.configure(state=NORMAL)
    root.config(bg="#F0F0F0")
    recorder_thread = None
    threading.Thread(target=gesture_start_thread, args=(root, camera, switch, settings)).start()
    exit_handler_thread = threading.Thread(target=stop_thread,args=(root,))
    exit_handler_thread.start()

def stop_thread(root):
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
    if UI_open[0]:
        root.config(bg="#F0F0F0")
    output.close()

    ##############

    get_text_feedback("summary.wav", root) if not (setting_params["live_feedback_on"] or setting_params["voice_on"]) else None

    today_string = str(datetime.now())
    update_log(today_string) if setting_params["username"] != "" else None

    last_file_counter = temp

    if setting_params["GET_SUMMARY"] and setting_params["username"] != "":
        with open(setting_params["username"] + ".json", "r") as f:
            logs = json.load(f)
            compose_summary(logs)
            
    if setting_params["CAN_SEND_EMAIL"]:
        send_message(compose_message(output_dic), setting_params["RECEIVER_EMAILS"])


def settings_click(root, camera, switch, settings, positionRight, positionDown):
    global UI_open
    UI_open[0] = False
    settings_win(root, positionRight, positionDown)
    UI_open[0] = True
    threading.Thread(target=gesture_start_thread, args=(root, camera, switch, settings)).start()