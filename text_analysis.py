import myspsolution as mysp
import speech_recognition as sr
from speaker import *
import os

AVERAGE_SYLLABLES_PER_WORD = 2
dir_path = os.path.dirname(os.path.realpath(__file__))

# Note filename must be in same directory as myspsolution.praat

def convert_to_words_per_min(syllables_per_sec):
    return syllables_per_sec*60*AVERAGE_SYLLABLES_PER_WORD

def get_speech_rate(filename="record_tmp"):
   return mysp.mypssr(filename, dir_path)


def get_summary(filename="record_tmp"):
   return mysp.mysptotal(filename, dir_path)


def get_articulation_rate(filename="record_tmp"):
   return mysp.myspatc(filename, dir_path)


def get_num_pauses(filename="record_tmp"):
   return mysp.mysppaus(filename, dir_path)


def get_num_syllables(filename="record_tmp"):
   return mysp.myspsyl(filename, dir_path)


def get_gender(filename="record_tmp"):
   return mysp.myspgend(filename, dir_path)


def get_words(filename="record_tmp"):
    AUDIO_FILE = (filename + ".wav")
    # use the audio file as the audio source

    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        # reads the audio file. Here we use record instead of
        # listen
        audio = r.record(source)

    try:
        print("The audio file contains: " + r.recognize_google(audio))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e} ")

def check_speech_rate(filename, desired_rate):
    sr = convert_to_words_per_min(get_speech_rate(filename))
    if sr > desired_rate:
        load_speech("You are speaking too fast. Speak slower.")
        unload_speech()

def check_filler_words(filename, filler_words=[]):
    if filler_words:
        words = get_words(filename)
        illegals = set(words).intersection(filler_words)
        if illegals:
            load_speech(f"Careful, you said the word {', '.join(illegals[:-1])} and {illegals[-1]}.")
            unload_speech()
    else:
        pass

def compose_text_summary(criterion={"speech_rate": True, "filler_words": True}):
    msg = []

