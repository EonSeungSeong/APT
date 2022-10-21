import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import xgboost as xgb


model = xgb.XGBClassifier()
model.load_model('_model/model_ssc.txt')
ssc_counter = 0
ssc_flag = False

def ctr_ssc(op_keypoint):
    global ssc_flag
    global ssc_counter
    global model  

    prd = model.predict(op_keypoint)
    print("ssc:",prd)

    if prd == 14 :
        ssc_flag = True
        # print(model.predict(temp))

    if ssc_flag and prd == 26:
        ssc_flag = False
        ssc_counter += 1
        
    return ssc_counter