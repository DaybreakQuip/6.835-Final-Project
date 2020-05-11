# 6.835-Final-Project
6.835 Final Project 6.UAssist
## Table of Contents

1. **main.py** - Run this file to start our system. This file initializes the main UI, which also links to the different functions in the other files. It also initalizes the camera used in gesture/motion detection.
2. **record.py** - This file handles recording the user's speech and saving it to a file.
3. **myspsolution.py** - main file for my-voice-analysis the library.
4. **myspsolution.praat** - supplementary file to (3) which is required for the library to run.
5. **speaker.py** - file used to generate audio for live voice feedback.
6. **mailer.py** - file used to email the summary to the user.
7. **gesture_analysis.py** - main file where all the functions necessary for motion detection/gesture analysis is contained.
8. **VGG_cross_validated.h5** - model used for gesture analysis.
9. **output.json** - output file used for mailer.
10. **text_analysis.py** - file containing all functions used to convert speech to text, as well as functions for detecting filler words and analyzing speed of audio file.
11. **gesture_handler.py** - file containing code that links UI to gesture analysis/starts gesture analysis.
12. **text_handler.py** - file containing code that links UI to text analysis/starts text analysis.
13. **settings.json** - contains user settings for the system, including email, filler words, stop word etc.
14. **settings_ui.py** - file containing all the settings parameters needed as well as other variables for the system. Contains code for the UI of settings.
15. **start_stop_handler.py** - file containg most of the code that actually starts/ends program (as well as code that signals the functions that analyzes) and handles the cleanup after the program ends.
16. **timer_handler.py** - file for the stopwatch shown in the UI.
17. **daboki.json** - file containing user data.
18. **abstract-img.png** - image for UI.
