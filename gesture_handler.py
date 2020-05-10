from gesture_analysis import *
from settings_ui import settings_win, setting_params, desired_rate, output_dic
import threading


motion_inform = [False]


gesture_model_filename = './VGG_cross_validated.h5'
gesture_model, gesture_graph, gesture_session = init_keras_thread(gesture_model_filename)
bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)

def get_gesture_feedback(camera):
    gesture_thread = threading.Thread(target=analyze_gesture,args=(capture_image(camera, bgModel), \
        gesture_model, gesture_graph, gesture_session, output_dic, setting_params["live_feedback_on"]))
    gesture_thread.start()

def get_motion_feedback(camera, root):
    motion_inform[0] = True
    motion_thread = threading.Thread(target=capture_motion, args=(camera, motion_inform, setting_params["live_feedback_on"], setting_params["voice_on"], root))
    motion_thread.start()

