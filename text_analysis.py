import myspsolution as mysp
import speech_recognition as sr
from speaker import *
import os

AVERAGE_SYLLABLES_PER_WORD = 1
dir_path = os.path.dirname(os.path.realpath(__file__))

# Note filename must be in same directory as myspsolution.praat

def convert_to_words_per_min(syllables_per_sec):
    if syllables_per_sec == None:
        return 130.0
    return syllables_per_sec*60/AVERAGE_SYLLABLES_PER_WORD

def get_speech_rate(filename="recording_"):
    try:
        return float(mysp.myspsr(filename, dir_path))
    except:
        return None


def get_summary(filename="recording_"):
   return mysp.mysptotal(filename, dir_path)


def get_articulation_rate(filename="recording_"):
   return float(mysp.myspatc(filename, dir_path))


def get_num_pauses(filename="recording_"):
   return float(mysp.mysppaus(filename, dir_path))


def get_num_syllables(filename="recording_"):
   return float(mysp.myspsyl(filename, dir_path))


def get_words(filename="recording_"):
    AUDIO_FILE = (filename + ".wav")
    # use the audio file as the audio source

    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        # reads the audio file. Here we use record instead of
        # listen
        audio = r.record(source)

    try:
        print("The audio file contains: " + r.recognize_google(audio))
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e} ")

    return

def check_speech_rate(audio_filename, desired_rate, output_dic):
    sr = convert_to_words_per_min(get_speech_rate(audio_filename))
    output_dic["AVG_SPEECH_RATE"] = (output_dic["AVG_SPEECH_RATE"] + sr) / 2.
    if sr > desired_rate:
        load_speech("You are speaking too fast. Speak slower.")
        unload_speech()

def check_filler_words(audio_filename, forbidden_words, output_dic):
    if not forbidden_words:
        forbidden_words = ["so", "um", "like", "literally", "basically", "well"]
    words = get_words(audio_filename).split(" ")
    illegals = list(set(words).intersection(forbidden_words))
    if illegals:
        if len(illegals) > 1:
            load_speech(f"Careful, you said the word {', '.join(illegals[:-1])} and {illegals[-1]}.")
        else:
            load_speech(f"Careful, you said the word {illegals[-1]}.")
        unload_speech()
        output_dic["SAID_ILLEGALS"] = list(set(output_dic["SAID_ILLEGALS"].append(illegals)))

