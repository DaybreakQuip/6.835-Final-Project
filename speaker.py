import pyttsx3

ENGINE = pyttsx3.init()

""" RATE """
rate = ENGINE.getProperty('rate')  # getting details of current speaking rate
ENGINE.setProperty('rate', 150)  # setting up new voice rate

""" VOLUME """
volume = ENGINE.getProperty(
    'volume')  #getting to know current volume level (min=0 and max=1)
ENGINE.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

""" VOICE """
voices = ENGINE.getProperty('voices')  #getting details of current voice
ENGINE.setProperty(
    'voice',
    voices[0].id)  #changing index, changes voices. o for male. 1 for female


def load_speech(text):
    ENGINE.say(text)


def unload_speech():
    ENGINE.runAndWait()