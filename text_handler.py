import threading
from settings_ui import setting_params, output_dic, desired_rate
from text_analysis import *

def get_text_feedback(audio_filename, root):
    sr_thread = threading.Thread(target=check_speech_rate,args=(audio_filename,desired_rate, output_dic, setting_params["live_feedback_on"], setting_params["voice_on"], root))
    sr_thread.start()
    filler_thread = threading.Thread(target=check_filler_words,args=(audio_filename,setting_params["forbidden"], output_dic, setting_params["live_feedback_on"],setting_params["voice_on"], root))
    filler_thread.start()