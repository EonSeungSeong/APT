import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import xgboost as xgb


model = xgb.XGBClassifier()
model.load_model('_model/model_gm.txt')
gm_counter = 0
gm_flag = False

def ctr_gm(op_keypoint):
    global gm_flag
    global gm_counter
    global model  

    prd = model.predict(op_keypoint)
    print("gm:",prd)

    if prd == 7:
        gm_flag = True
        # print(model.predict(temp))

    if gm_flag and prd == 4:
        gm_flag = False
        gm_counter += 1
        
    return gm_counter