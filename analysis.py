import myspsolution as mysp
import os
import speech_recognition as sr

dir_path = os.path.dirname(os.path.realpath(__file__))

p="recording_tmp" # Audio File title
mysp.mysppaus(p,dir_path)

AUDIO_FILE = ("record_tmp.wav")

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
    print("Could not request results from Google Speech Recognition service; {0} ".format(e))
# Note filename must be in same directory as myspsolution.praat


def get_speech_rate(filename):
    mysp.mypssr(filename, dir_path)


def get_summary(filename):
    mysp.mysptotal(filename, dir_path)


def get_articulation_rate(filename):
    mysp.myspatc(filename, dir_path)


def get_num_pauses(filename):
    mysp.mysppaus(filename, dir_path)


def get_num_syllables(filename):
    mysp.myspsyl(filename, dir_path)


def get_gender(filename):
    mysp.myspgend(filename, dir_path)
