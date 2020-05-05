from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
import json
import os

setting_params = {"forbidden": [],
                  "username": "daboki",
                  "desired_rate_mode": "slow",
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
    settings_window.geometry("300x500""+{}+{}".format(positionRight + 50, positionDown + 100))

    words_label = Label(settings_window, text="Illegal Words Entry:", font=("Courier",10))
    e = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e.insert(END, ' '.join(setting_params["forbidden"]))
    words_label.pack()
    e.pack()

    def update_words():
        search_param = e.get("1.0","end-1c")
        setting_params["forbidden"].clear()
        setting_params["forbidden"].extend(search_param.split())
        print(setting_params)
        update_settings()


    list_of_words = Button(settings_window, text='Update', height=2, width=20, command=update_words)
    list_of_words.pack()


    email_label = Label(settings_window, text="Send Report to Email?:", font=("Courier",10))
    email_option = Combobox(settings_window, values=["Send Report", "Don't Send Report"])
    email_label.pack()
    email_option.pack()

    address_label = Label(settings_window, text="Enter Email Addresses:", font=("Courier",10))
    e_address = ScrolledText(settings_window, width=30, height=10, wrap=WORD)
    e_address.insert(END, ' '.join(setting_params["RECEIVER_EMAILS"]))

    def update_address():
        search_param = e_address.get("1.0","end-1c")
        setting_params["RECEIVER_EMAILS"].clear()
        setting_params["RECEIVER_EMAILS"].extend(search_param.split())
        update_settings()

    address_label.pack()
    address_update = Button(settings_window, text='Update', height=2, width=20, command=update_address)
    e_address.pack()
    address_update.pack()

    def email_option_selected(event):
        if email_option.get() == "Send Report":
            setting_params["CAN_SEND_EMAIL"] = True
        else:
            setting_params["CAN_SEND_EMAIL"] = False
        update_settings()

    email_option.bind("<<ComboboxSelected>>", email_option_selected)

    settings_window.transient(root)
    settings_window.grab_set()
    root.wait_window(settings_window)
