import copy
import cv2
import numpy as np
from keras.models import load_model
import pygame
import tensorflow as tf
import time

prediction = ''
action = ''
score = 0

cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.8  # start point/total width
threshold = 60  # binary threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0

# variableslt
triggerSwitch = False  # if true, keyboard simulator works

sentiment_names: {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "sad",
    4: "surprise",
    5: "neutral"
}

gesture_names = {0: 'Fist', 1: 'L', 2: 'Okay', 3: 'Palm', 4: 'Peace'}

def init_keras_thread(model_filename=None):
    thread_graph = tf.Graph()
    with thread_graph.as_default():
        thread_session = tf.Session()
        with thread_session.as_default():
            model = load_model(model_filename)
            graph = tf.get_default_graph()
    return [model, graph, thread_session]


def remove_background(bgModel, frame):
    fgmask = bgModel.apply(frame, learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def predict_rgb_image_vgg(model, image):
    image = np.array(image, dtype='float32')
    image /= 255
    pred_array = model.predict(image)
    result = np.argmax(pred_array)
    score = float("%0.2f" % (max(pred_array[0]) * 100))
    return result, score


def capture_image(camera, bgModel, mode="gesture"):
    # Camera
    ret, frame = camera.read()

    if mode == "gesture":
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])),
                      (255, 0, 0), 2)

        # Run once background is captured

        img = remove_background(bgModel, frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                  int(cap_region_x_begin *
                      frame.shape[1]):frame.shape[1]]  # clip the ROI

        # cv2.imshow('mask', img)

        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        # cv2.imshow('blur', blur)
        ret, thresh = cv2.threshold(blur, threshold, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh
    else:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def analyze_gesture(thresh, model, graph, session):
    # copies 1 channel BW image to all 3 RGB channels
    target = np.stack((thresh, ) * 3, axis=-1)
    target = cv2.resize(target, (224, 224))
    target = target.reshape(1, 224, 224, 3)
    with graph.as_default():
        with session.as_default():
            prediction, score = predict_rgb_image_vgg(model, target)
            prediction = gesture_names[prediction]
            if prediction == 'Palm':
                print("Palm")
            elif prediction == 'Fist':
                print('Fist')
            elif prediction == 'L':
                print("L")
            elif prediction == 'Okay':
                print("Okay")
            elif prediction == 'Peace':
                print("Prace")
            else:
                print("nothi")


def analyze_sentiment(target, model, graph, session):
    target = cv2.resize(target, (48, 48))
    target = target.reshape(-1, 48, 48, 1)
    with graph.as_default():
        with session.as_default():
            prediction, score = predict_rgb_image_vgg(model, target)
            if prediction == 0:
                print("angry")
            elif prediction == 1:
                print("disgust")
            elif prediction == 3:
                print("sad")
            elif prediction == 4:
                print("sad")
            elif prediction == 5:
                print("surprise")
            else:
                print("neutral")
