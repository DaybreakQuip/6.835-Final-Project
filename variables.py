import os

dir_path = os.path.dirname(os.path.realpath(__file__))

runner1 = None
counter = 0
last_file_counter = 0
tmp_prefix_name = "recording_"
state = False
time_count = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'
motion_inform = [False]

# Must be included in settings:
forbidden = []
CAN_SEND_EMAIL = False
GET_SUMMARY = False
RECEIVER_EMAILS = [""]
live_feedback_on = True
username = "daboki"
desired_rate_mode = "slow"