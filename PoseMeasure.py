import numpy as np
import pandas as pd
import xgboost as xgb

model = xgb.XGBClassifier()
# model.load_model('model_ssc.txt')
model.load_model('model_cl.txt')
# model.load_model('model_gm.txt')

flag = False
counter = 0


def return_model():
    # model = xgb.XGBClassifier()
    # model.load_model('model_cl.txt')
    global model
    return model


def ctr_ssc(prd):
    global flag
    global counter

    if prd == 26:
        flag = True
        # print(model.predict(temp))

    if flag and prd == 14:
        flag = False
        counter += 1
        print("count!", counter)


def ctr_gm(prd):
    global flag
    global counter

    if prd == 1:
        flag = True
        # print(model.predict(temp))

    if flag and prd == 7:
        flag = False
        counter += 1
        print("count!", counter)


def ctr_cl(kpt):
    global flag
    global counter
    
    prd = model.predict(kpt)
    if prd == 1:
        flag = True
        # print(model.predict(temp))

    if flag and prd == 2:
        flag = False
        counter += 1
        print("count!", counter)

    return counter


def prd_proba(kpt):
    return model.predict_proba(kpt)


if __name__ == '__main__':
    print(ctr_cl(None))
    print(ctr_)