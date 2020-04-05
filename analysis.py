import myspsolution as mysp
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

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
