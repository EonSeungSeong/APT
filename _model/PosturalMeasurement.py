# import xgboost as xgb
#
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
#
#
# def get_clf_eval(y_test, pred=None):
#     cf = confusion_matrix(y_test, y_pred)
#     acc = accuracy_score(y_test, y_pred)
#     prc = precision_score(y_test, y_pred, average='micro')
#     recall = recall_score(y_test, y_pred, average='micro')
#     f1 = f1_score(y_test, y_pred, average='micro')
#
#     print(cf)
#     print(f"""
#     정확도 {format(acc, '.4f')}
#     정밀도 {format(prc, '.4f')}
#     재현율 {format(recall, '.4f')}
#     F1     {format(f1, '.4f')}
#     """)
#
#
# model = xgb.XGBClassifier()
# model.load_model("_model/model.txt")
#
# def out_y_pred (df_new):
#     return model.predict(df_new)