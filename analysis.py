import myspsolution as mysp
import speech_recognition as sr
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Note filename must be in same directory as myspsolution.praat


def get_speech_rate(filename="record_tmp"):
    mysp.mypssr(filename, dir_path)


def get_summary(filename="record_tmp"):
    mysp.mysptotal(filename, dir_path)


def get_articulation_rate(filename="record_tmp"):
    mysp.myspatc(filename, dir_path)


def get_num_pauses(filename="record_tmp"):
    mysp.mysppaus(filename, dir_path)


def get_num_syllables(filename="record_tmp"):
    mysp.myspsyl(filename, dir_path)


def get_gender(filename="record_tmp"):
    mysp.myspgend(filename, dir_path)


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
