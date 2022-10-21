
from flask import Blueprint, url_for, render_template, flash, request,session,g,Response
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect
import xgboost as xgb

from apt import db
import cv2
import mediapipe as mp
import pyttsx3
import numpy as np
import pandas as pd
import time
import recommand
from apt.models import User,Predata,Basictest,Result,Test
from apt.views.auth_views import login_required
from _model.exer_cl import temp_ctr_cl,cl_flag,cl_counter
from _model.exer_ssc import ctr_ssc,ssc_flag,ssc_counter
from _model.exer_gm import ctr_gm,gm_flag,gm_counter

bp = Blueprint('video', __name__, url_prefix='/')

# ajax 통신 변수
tem_message = "temporary"
final_message = "prediction result"

tem_set = "temporary"
final_set = "prediction set"

tem_exer = "temporary"
final_exer = "prediction exer"

g_count = 0
g_set = 0
g_cor = 0
g_exer = "no"
next_page = 0  # 향후 pre랑 mea 구분역할

# 카메라 테스트 페이지
@bp.route('/video')
@login_required
def video():
    global next_page
    result = recommand.result
    if  Basictest.query.filter(Basictest.user_id==g.user.id).count()==0: #Basictest안했을 경우
        next_page = 1
    else :
        next_page = 2
    return render_template('video.html',resultReceived=sendResult())
            
# 테스트측정결과 수정 페이지
@bp.route('/input_health')
@login_required
def index():
    #DB에서 데이터 가져오는 코드
    #count=Basictest.query.filter(Basictest.user_id==g.user.id).count() #기초체력테스트 데이터 중 사용자가 만든 Basictest개수
    b=Basictest.query.filter(Basictest.user_id==g.user.id).first() #Basictest는 일단 한번만 하게 해놨어,,,
    print(b._count)
    #print(count)
    #b=Basictest.query.get(count) #저장 값 중 제일 마지막 행 정보 전부 가져옴 ->1나옴
    _count=b._count 
    example=20
    percent_count=int(_count/example*100)
    ###################################################
    if _count<10:
        level='입문자'
    elif _count<=15:
        level='초보자'
    elif _count<=20:
        level='중급자'
    else:
        level='전문가'
    return render_template('input_health.html',_count=_count,percent_count=percent_count,level=level)

# 추천결과 페이지
@bp.route('/recommend_exse',methods=('GET','POST'))
@login_required
def recommend_view():
    result = recommand.result
    #DB에서 데이터 가져오는 코드
    # count=Predata.query.filter(Predata.user_id==g.user.id).count() #기초체력테이블의 행 수
    # print(count)
    b=Basictest.query.filter(Basictest.user_id==g.user.id).first() #지금 사용하는 사람이 제일 처음한 기초체력테스트 결과 값
    p=Predata.query.filter(Predata.user_id==g.user.id).first()
    #print(b.user_level)
    if b.user_level==1: #입문자
        set_= 1
        count_=3
    elif b.user_level==2: #초보자
        set_= 2
        count_=3
    elif b.user_level==3: #중급자
        set_= 3
        count_=3
    else:#전문가
        set_= 4
        count_=3

    if request.method == 'POST':
        r=Result(user=g.user, predata_id=p.id,basictest_id=b.id,
            ex_name1=result[0], re_count1=count_, re_set1 = set_, kcal1=int(3*(count_*set_)),
            ex_name2=result[1],re_count2=count_, re_set2 = set_, kcal2=int(1*(count_*set_)),
            ex_name3=result[2],re_count3=count_, re_set3 = set_, kcal3=int(5*(count_*set_)))
        db.session.add(r)
        
        t=Test(user=g.user, ex_name1=result[0], ex_name2=result[1], ex_name3=result[2],count=count_,sett=set_)
        db.session.add(t)
        db.session.commit()
        return redirect((url_for('video.video')))
    return render_template('recommend_exse.html', resulthtml1=result[0],resulthtml2=result[1],resulthtml3=result[2],set_=set_, count_=count_)

# 측정 페이지
@bp.route('/measurement')
@login_required
def measure_view():
        #DB필터링
    test_data=Test.query.filter(Test.user_id==g.user.id).all()
    _list=[]
    for i in range(len(test_data)):
        _list.append(test_data[i].id)
    mx=max(_list) #id중 최댓값=마지막 인덱스
    data=Test.query.get(mx)
    t_count = data.count
    t_set = data.sett
    name1=data.ex_name1
    name2=data.ex_name2
    name3=data.ex_name3
    print(t_count)
    print(t_set)
    print(name1)
    print(name2)
    print(name3)
    return render_template('measurement.html',resultReceived=sendResult(),resultSet=sendSet(),resultExer=sendExer(),t_count=t_count,t_set=t_set)

# 기초 체력 측정 페이지
@bp.route('/premeasure',methods=('GET','POST'))
@login_required
def premeasure_view():
    if  request.method == 'POST' :
        temp_level = leveltest(g_count)
        Basictest.query.filter(Basictest.user_id==g.user.id).update({'_count' : g_count})
        Basictest.query.filter(Basictest.user_id==g.user.id).update({'user_level' : temp_level})
        save=Basictest(user=g.user,_count=g_count,user_level=temp_level)
        db.session.add(save)
        db.session.commit()
        return redirect('/input_health')

    return render_template('premeasure.html',resultReceived=sendResult())

# 측정 결과 페이지
@bp.route('/result')
def result_view():
    #resut에 퍼센트는 나중에 다만들고 해놓을게!
    
    #r_count=Result.query.filter(Result.user_id==g.user.id).count()
    #print(r_count)
    test=Result.query.filter(Result.user_id==g.user.id).all()
    _list=[]
    for i in range(len(test)):
        _list.append(test[i].id)
    mx=max(_list)
    r=Result.query.get(mx)
    re_count1= r.re_count1
    #print(re_count1)
    re_count2= r.re_count2
    re_count3= r.re_count3

    re_set1= r.re_set1
    re_set2= r.re_set2
    re_set3= r.re_set3

    ex_name1=r.ex_name1
    ex_name2=r.ex_name2
    ex_name3=r.ex_name3

    kcal1=r.kcal1
    kcal2=r.kcal2
    kcal3=r.kcal3
    if request.method == 'POST':
        redirect((url_for('main.index')))
    return render_template('result.html',re_count1=re_count1,re_count2=re_count2,re_count3=re_count3,re_set1=re_set1,re_set2=re_set2,re_set3=re_set3,ex_name1=ex_name1,ex_name2=ex_name2,ex_name3=ex_name3,kcal1=kcal1,kcal2=kcal2,kcal3=kcal3)



########### 함수 ##############

# 카메라 테스트 페이지 내 카메라 호출 함수
@bp.route('/checkSkeleton')
@login_required
def checkSkeleton():
    return Response(check_skeleton(),mimetype='multipart/x-mixed-replace; boundary=frame')

# 기초체력 측정 페이지 내 카메라 호출 함수
@bp.route('/checkBasic')
def checkBasic():
    return Response(check_basic(),mimetype='multipart/x-mixed-replace; boundary=frame')

# 측정 페이지 내 카메라 호출 함수
@bp.route('/checkRoutine')
def checkRoutine():
    # tmp=Test.query.filter(Test.user_id==g.user.id)
    tmp=Test.query.filter(Test.user_id==g.user.id).all()
    _list=[]
    for i in range(len(tmp)):
        _list.append(tmp[i].id)
    mx=max(_list) #id중 최댓값=마지막 인덱스
    data=Test.query.get(mx)
    t_count = data.count
    t_set = data.sett
    name1=data.ex_name1
    name2=data.ex_name2
    name3=data.ex_name3
    t_exer = [name1,name2,name3]
    return Response(check_routine(t_exer,t_count,t_set),mimetype='multipart/x-mixed-replace; boundary=frame')    

# ajax 통신 함수
@bp.route("/sendResult")
def sendResult():
    global tem_message, final_message

    if tem_message == "temporary":
        final_message = "no prediction yet"

    else:
        final_message = tem_message

    return final_message

# ajax 통신 함수(set용)
@bp.route("/sendSet")
def sendSet():
    global tem_set, final_set
    if tem_set == "temporary":
        final_set = "no prediction yet"
    
    else:
        final_set = tem_set

    return final_set

# ajax 통신 함수(운동용)
@bp.route("/sendExer")
def sendExer():
    global tem_exer, final_exer
    if tem_exer == "temporary":
        final_set = "no prediction yet"
    
    else:
        final_exer = tem_exer

    return final_exer

def check_skeleton():

    global tem_message
    global next_page

    voice_output('Skeleton측정을 시작합니다. 몸 전체가 카메라에 나오게 해주세요.')

    camera=cv2.VideoCapture(1)
    #camera=cv2.VideoCapture(0,cv2.CAP_DSHOW) 웹캠코드 사용-언승
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        
        flag = False
        word = ""
        color = (0,0,255)
     
        while True:

            ## read the camera frame
            success, frame = camera.read()
            if not success:
                continue
            else:              
                
                frame.flags.writeable = False    # 성능 향상을 위해 이미지 쓰기불가시켜 참조로 전달
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)   # pose 검출

                frame.flags.writeable = True    # 다시 쓰기 가능으로 변경
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                min_i = 1.0

                if results.pose_landmarks:
                    for i in results.pose_landmarks.landmark:
                        min_i = min(min_i, i.visibility)

                    if min_i > 0.6: # 0.5 ~ 0.6사이가 좋을듯
                        flag = True

                    if flag:
                        # 기초체력 측정페이지 or 측정 페이지로 넘어가야함
                        word = "good"
                        if next_page == 1:
                            tem_message = "성공!"
                        elif next_page == 2:
                            tem_message = "성공!!"
                        
                        color = (255,0,0)
                        mp_drawing.draw_landmarks(
                            frame,
                            results.pose_landmarks,
                            mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                        
                    else:                        
                        word = "please go back"
                        tem_message = "뒤로 가주세요"
                        


                frame = cv2.flip(frame, 1)
                frame = cv2.putText(frame, word,(100,70),cv2.FONT_HERSHEY_SIMPLEX,1.0,color,3,cv2.LINE_AA)

                ret, buffer =cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

idx = np.array(['Nose_x', 'Left Eye_x', 'Right Eye_x', 'Left Ear_x', 'Right Ear_x',
            'Left Shoulder_x', 'Right Shoulder_x', 'Left Elbow_x', 'Right Elbow_x',
            'Left Wrist_x', 'Right Wrist_x', 'Left Hip_x', 'Right Hip_x', 'Left Knee_x',
            'Right Knee_x', 'Left Ankle_x', 'Right Ankle_x', 'Neck_x', 'Left Palm_x',
            'Right Palm_x', 'Back_x', 'Waist_x', 'Left Foot_x', 'Right Foot_x',
            'Nose_y', 'Left Eye_y', 'Right Eye_y', 'Left Ear_y', 'Right Ear_y',
            'Left Shoulder_y', 'Right Shoulder_y', 'Left Elbow_y', 'Right Elbow_y',
            'Left Wrist_y', 'Right Wrist_y', 'Left Hip_y', 'Right Hip_y', 'Left Knee_y',
            'Right Knee_y', 'Left Ankle_y', 'Right Ankle_y', 'Neck_y', 'Left Palm_y',
            'Right Palm_y', 'Back_y', 'Waist_y', 'Left Foot_y', 'Right Foot_y'])
       
def check_routine(t_exer,t_count,t_set):

    global tem_message
    global tem_set
    global tem_exer

    global idx
    global g_count  # 현재 count
    global g_set    # 현재 set
    global g_cor    # 현재 정확도
    global g_exer   # 현재 운동명    

    print(t_exer)
    g_count = 0
    g_set = 0
    tem_message = str(g_count)
    i = 0
    g_exer = t_exer[0]     
    acc = 0
    check = 0
    word =""

    # voice_output('안녕하세요 오늘도 화이팅입니다')

    camera=cv2.VideoCapture(1)
    # camera=cv2.VideoCapture(0,cv2.CAP_DSHOW) 웹캠코드 사용-언승
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        
                
        while True:

            ## read the camera frame
            success, frame = camera.read()
            if not success:
                continue
            else:              
                
                frame.flags.writeable = False    # 성능 향상을 위해 이미지 쓰기불가시켜 참조로 전달
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)   # pose 검출

                frame.flags.writeable = True    # 다시 쓰기 가능으로 변경
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                
                if results.pose_landmarks:                        
                    op_keypoint = pd.DataFrame(np.array(change_keypoint(results)), index=idx).T
                    
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    if g_exer == "크로스 런지":
                        g_count,acc = temp_ctr_cl(op_keypoint)
                        word = "cross lunge"

                    elif g_exer == "스탠딩사이드":
                        g_count = ctr_ssc(op_keypoint)
                        word = "standing side"

                    elif g_exer == "굿모닝":
                        g_count = ctr_gm(op_keypoint)
                        word = "good morning"

                    if g_count == t_count :
                        g_count -= 0
                        g_set += 1
                    
                    if g_set > t_set :
                        i += 1
                        if i == 3:
                            # 운동종료, html 에서 강제클릭이벤트 발생 후 mea로 넘어가기
                            return 0
                        g_exer = t_exer[i]
                        g_count = 0
                        g_set = 0
                    
                    # check += 1

                    # if check % 50 == 0:
                    #     g_count += 1
                    #     if g_count > t_count :
                    #         g_count -= t_count
                    #         g_set += 1


                frame = cv2.flip(frame, 1)
                frame = cv2.putText(frame, str(g_count),(80,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),14,cv2.LINE_AA)
                frame = cv2.putText(frame, str(g_count),(80,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,255,0),7,cv2.LINE_AA)

                frame = cv2.putText(frame, str(word),(150,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),14,cv2.LINE_AA)
                frame = cv2.putText(frame, str(word),(150,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(255,255,0),7,cv2.LINE_AA)

                tem_message = str(g_count)
                tem_set = str(g_set)
                tem_exer = str(g_exer)

                ret, buffer =cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()
                
        
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def change_keypoint(results):
    op_keypoint = [results.pose_landmarks.landmark[0].x,  # <<OpenPose기준>> 0번값 Nose
                    results.pose_landmarks.landmark[2].x,  # 1번값 Left Eye
                    results.pose_landmarks.landmark[5].x,  # 2번값 Right Eye
                    results.pose_landmarks.landmark[7].x,  # 3번값 Left Ear
                    results.pose_landmarks.landmark[8].x,  # 4번값 Right Ear
                    results.pose_landmarks.landmark[11].x,  # 5번값 Left Shoulder
                    results.pose_landmarks.landmark[12].x,  # 6번값 Right Shoulder
                    results.pose_landmarks.landmark[13].x,  # 7번값 Left Elbow
                    results.pose_landmarks.landmark[14].x,  # 8번값 Right Elbow
                    results.pose_landmarks.landmark[15].x,  # 9번값 Left Wrist
                    results.pose_landmarks.landmark[16].x,  # 10번값 Right Wrist
                    results.pose_landmarks.landmark[23].x,  # 11번값 Left Hip
                    results.pose_landmarks.landmark[24].x,  # 12번값 Right Hip
                    results.pose_landmarks.landmark[25].x,  # 13번값 Left Knee
                    results.pose_landmarks.landmark[26].x,  # 14번값 Right Knee
                    results.pose_landmarks.landmark[27].x,  # 15번값 Left Ankle
                    results.pose_landmarks.landmark[28].x,  # 16번값 Right Ankle
                    0,  # 17번값 Neck
                    0,  # 18번값 Left Palm -
                    0,  # 19번값 Right Palm -
                    0,  # 20번값 Back ?
                    0,  # 21번값 Waist ?
                    results.pose_landmarks.landmark[31].x,  # 22번값 Left Foot
                    results.pose_landmarks.landmark[32].x,  # 23번값 Right Foot

                    results.pose_landmarks.landmark[0].y,  # <<OpenPose기준>> 24번값 Nose
                    results.pose_landmarks.landmark[2].y,  # 25번값 Left Eye
                    results.pose_landmarks.landmark[5].y,  # 26번값 Right Eye
                    results.pose_landmarks.landmark[7].y,  # 27번값 Left Ear
                    results.pose_landmarks.landmark[8].y,  # 28번값 Right Ear
                    results.pose_landmarks.landmark[11].y,  # 29번값 Left Shoulder
                    results.pose_landmarks.landmark[12].y,  # 30번값 Right Shoulder
                    results.pose_landmarks.landmark[13].y,  # 31번값 Left Elbow
                    results.pose_landmarks.landmark[14].y,  # 32번값 Right Elbow
                    results.pose_landmarks.landmark[15].y,  # 33번값 Left Wrist
                    results.pose_landmarks.landmark[16].y,  # 34번값 Right Wrist
                    results.pose_landmarks.landmark[23].y,  # 35번값 Left Hip
                    results.pose_landmarks.landmark[24].y,  # 36번값 Right Hip
                    results.pose_landmarks.landmark[25].y,  # 37번값 Left Knee
                    results.pose_landmarks.landmark[26].y,  # 38번값 Right Knee
                    results.pose_landmarks.landmark[27].y,  # 39번값 Left Ankle
                    results.pose_landmarks.landmark[28].y,  # 40번값 Right Ankle
                    0,  # 41번값 Neck
                    0,  # 42번값 Left Palm 
                    0,  # 43번값 Right Palm 
                    0,  # 44번값 Back 
                    0,  # 45번값 Waist 
                    results.pose_landmarks.landmark[31].y,  # 46번값 Left Foot
                    results.pose_landmarks.landmark[32].y]  # 47번값 Right Foot
    # Neck
    op_keypoint[17] = (results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x) / 2
    op_keypoint[41] = (results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y) / 2

    # Left Palm
    op_keypoint[18] = (results.pose_landmarks.landmark[20].x + results.pose_landmarks.landmark[18].x +
                    results.pose_landmarks.landmark[16].x) / 3
    op_keypoint[42] = (results.pose_landmarks.landmark[20].y + results.pose_landmarks.landmark[18].y +
                    results.pose_landmarks.landmark[16].y) / 3
    # Right Palm
    op_keypoint[19] = (results.pose_landmarks.landmark[19].x + results.pose_landmarks.landmark[17].x +
                    results.pose_landmarks.landmark[15].x) / 3
    op_keypoint[43] = (results.pose_landmarks.landmark[19].y + results.pose_landmarks.landmark[17].y +
                    results.pose_landmarks.landmark[15].y) / 3
    # Back
    tmpx = (op_keypoint[17] - (
                (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x) / 2)) / 3
    tmpy = (op_keypoint[41] - (
                (results.pose_landmarks.landmark[23].y + results.pose_landmarks.landmark[24].y) / 2)) / 3

    op_keypoint[20] = op_keypoint[17] + tmpx
    op_keypoint[44] = op_keypoint[41] + tmpy

    # Waist
    op_keypoint[21] = op_keypoint[17] + (tmpx * 2)
    op_keypoint[45] = op_keypoint[41] + (tmpy * 2)

    return op_keypoint

def check_basic():

    global tem_message
    global g_count
      
    voice_output('기초체력을 측정합니다')

    g_count = 0
    fflag = True

    camera=cv2.VideoCapture(1)
    # camera=cv2.VideoCapture(0,cv2.CAP_DSHOW) 웹캠코드 사용-언승
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    check = 1

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:    
        
        while True:

            ## read the camera frame
            success, frame = camera.read()
            if not success:
                continue
            else:              
                
                frame.flags.writeable = False    # 성능 향상을 위해 이미지 쓰기불가시켜 참조로 전달
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)   # pose 검출

                frame.flags.writeable = True    # 다시 쓰기 가능으로 변경
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                
                if results.pose_landmarks:

                    landmarks = results.pose_landmarks.landmark
                    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                    angle_knee = calculate_angle(hip, knee, ankle)
                    knee_angle = 180-angle_knee

                    angle_hip = calculate_angle(shoulder, hip, knee)
                    hip_angle = 180-angle_hip

                    check += 1

                    if check % 70 == 0 and fflag ==True:
                        g_count += 1
                    
                    if g_count == 3:
                        fflag = False
                        


                    # # 카운팅 시작
                    # # 앉았을 경우 : check -1, count += 1
                    # if knee_angle > 70 and hip_angle > 70 and check == 1:
                    #     check *= -1
                    #     count += 1
                    
                    # # 서있을 경우 : check 1
                    # elif 70 >= knee_angle and 70 >= hip_angle and check == -1:
                    #     check *= -1
                        


                frame = cv2.flip(frame, 1)
                frame = cv2.putText(frame, str(g_count),(80,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,0),14,cv2.LINE_AA)
                frame = cv2.putText(frame, str(g_count),(80,70),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,255,0),7,cv2.LINE_AA)

                # Basictest.query.filter(Basictest.user_id==g.user.id).update({'_count' : (set*3) + count})
                # db.session.commit()

                tem_message = str(g_count)

                ret, buffer =cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')                    

def voice_output(sentence):

    speak = pyttsx3.init()
    speak.say(sentence)
    speak.runAndWait()
    speak.stop()
    return 0

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def leveltest(temp_count):
    if temp_count<10:
        level=1
    elif temp_count<=15:
        level=2
    elif temp_count<=20:
        level=3
    else:
        level=4
    return level
