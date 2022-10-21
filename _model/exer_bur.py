import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import xgboost as xgb


model = xgb.XGBClassifier()
model.load_model('_model/model_bur.txt')
bur_counter = 0
bur_flag = False

def ctr_bur(op_keypoint):
    global bur_flag
    global bur_counter
    global model  

    prd = model.predict(op_keypoint)

    if prd == 26:
        bur_flag = True
        # print(model.predict(temp))

    if bur_flag and prd == 14:
        bur_flag = False
        bur_counter += 1
        
    return bur_counter