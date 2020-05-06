from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
import json
import os

setting_params = {"forbidden": [],
                  "username": "daboki",
                  "desired_rate_mode": "slow",
                  "stop_phrase": "",
                  "CAN_SEND_EMAIL": False,
                  "GET_SUMMARY": False,
                  "RECEIVER_EMAILS": [""],
                  "live_feedback_on": True,
                  "voice_on": True}

if not os.path.exists("settings.json"):
    with open('settings.json', 'w') as outfile:
        json.dump(setting_params, outfile)
else:
    with open('settings.json') as f:
        setting_params = json.load(f)

def update_settings():
    with open('settings.json', 'w') as outfile:
        json.dump(setting_params, outfile)

def settings_win(root, positionRight, positionDown):
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x700""+{}+{}".format(positionRight + 40, positionDown + 60))

    words_label = Label(settings_window, text="Illegal Words Entry:", font=("Courier",10))
    e = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e.insert(END, ' '.join(setting_params["forbidden"]))

    stop_phrase_label = Label(settings_window, text="Stop Phrase:", font=("Courier",10))
    stop_phrase = ScrolledText(settings_window, width=30, height=5, wrap=WORD)
    stop_phrase.insert(END, setting_params["stop_phrase"])

    words_label.pack()
    e.pack()

    stop_phrase_label.pack()
    stop_phrase.pack()

    email_label = Label(settings_window, text="Send Report to Email?", font=("Courier",10))
    email_option = Combobox(settings_window, values=["Send Report", "Don't Send Report"])
    email_option.current(0 if setting_params["CAN_SEND_EMAIL"] else 1)

    live_feedback_label = Label(settings_window, text="Toggle Color Feedback:", font=("Courier",10))
    live_feedback_option = Combobox(settings_window, values=["Color On", "Color Off"])
    live_feedback_option.current(0 if setting_params["live_feedback_on"] else 1)

    voice_feedback_label = Label(settings_window, text="Toggle Voice Feedback:", font=("Courier",10))
    voice_feedback_option = Combobox(settings_window, values=["Voice On", "Voice Off"])
    voice_feedback_option.current(0 if setting_params["voice_on"] else 1)

    speech_rate_label = Label(settings_window, text="Desired Speech Rate", font=("Courier",10))
    speech_rate_option = Combobox(settings_window, values=["Slow", "Fast"])
    speech_rate_option.current(0 if setting_params["desired_rate_mode"] == "slow" else 1)



    email_label.pack()
    email_option.pack()

    live_feedback_label.pack()
    live_feedback_option.pack()

    voice_feedback_label.pack()
    voice_feedback_option.pack()

    speech_rate_label.pack()
    speech_rate_option.pack()

    address_label = Label(settings_window, text="Enter Email Addresses:", font=("Courier",10))
    e_address = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e_address.insert(END, ' '.join(setting_params["RECEIVER_EMAILS"]))

    def update_everything():
        search_param = e.get("1.0","end-1c")
        setting_params["forbidden"].clear()
        setting_params["forbidden"].extend(search_param.split())

        setting_params["stop_phrase"] = stop_phrase.get("1.0","end-1c")

        search_param = e_address.get("1.0","end-1c")
        setting_params["RECEIVER_EMAILS"].clear()
        setting_params["RECEIVER_EMAILS"].extend(search_param.split())
        update_settings()

    address_label.pack()
    update_all = Button(settings_window, text='Update', height=2, width=20, command=update_everything)
    e_address.pack()
    update_all.pack()

    def email_option_selected(event):
        if email_option.get() == "Send Report":
            setting_params["CAN_SEND_EMAIL"] = True
        else:
            setting_params["CAN_SEND_EMAIL"] = False

    def live_feedback_option_selected(event):
        if live_feedback_option.get() == "Color On":
            setting_params["live_feedback_on"] = True
        else:
            setting_params["live_feedback_on"] = False

    def voice_feedback_option_selected(event):
        if voice_feedback_option.get() == "Voice On":
            setting_params["voice_on"] = True
        else:
            setting_params["voice_on"] = False

    def speech_rate_option_selected(event):
        if speech_rate_option.get() == "Slow":
            setting_params["desired_rate_mode"] = "slow"
        else:
            setting_params["desired_rate_mode"] = "fast"

    email_option.bind("<<ComboboxSelected>>", email_option_selected)
    live_feedback_option.bind("<<ComboboxSelected>>", live_feedback_option_selected)
    voice_feedback_option.bind("<<ComboboxSelected>>", voice_feedback_option_selected)
    speech_rate_option.bind("<<ComboboxSelected>>", speech_rate_option_selected)


    settings_window.transient(root)
    settings_window.grab_set()
    root.wait_window(settings_window)
