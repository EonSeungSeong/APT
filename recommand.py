import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from apt.models import Predata
from datetime import datetime
import config
import sqlite3
from flask import g

# db table과 연결
connection = sqlite3.connect('apt.db')
# database와 communicate 하기 위한 코드
cursor = connection.cursor()
# 쿼리문 -> 여기에 CRUD 가능!
cursor.execute("SELECT * FROM Predata")
# print database rows
db_value = []
for row in cursor.execute("SELECT * FROM Predata"):
    db_value.append(row)
connection.close()
# 불러온 data를 dataframe화
df_db_value = pd.DataFrame(db_value, columns = ['id', 'user_id', 'shoulder', 'arm','chest', 'back', 'stomach', 'core', 'hip', 'thigh', 'body'])
# 신체 부위 가중치 값만 가져오기
df_w = df_db_value.iloc[[-1]]
df_weight = df_w[['shoulder', 'arm','chest', 'back', 'stomach', 'core', 'hip', 'thigh', 'body']]
#df_weight = pd.DataFrame(df_w)
# print specific rows
exercise = pd.read_excel('exercise.xlsx')
exercise.set_index('운동명', inplace=True)

# cosine similarity 계산
similarity = cosine_similarity(exercise, df_weight)
df = pd.DataFrame(data=similarity, index = exercise.index)
df.columns = ['similarity']
df.sort_values(by=['similarity'], ascending=False, inplace= True)
result = df[0:3].index
# except:
#     result = ["추천된 운동이 없습니다.", "추천된 운동이 없습니다.", "추천된 운동이 없습니다."]
