import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import xgboost as xgb


model = xgb.XGBClassifier()
model.load_model('_model/model_cl.txt')
cl_counter = 0
cl_flag = False


def temp_ctr_cl(op_keypoint):
    global cl_flag
    global cl_counter
    global model  

    prd = model.predict(op_keypoint)
    prob = model.predict_proba(op_keypoint)
    acc = 0
    print("cl:",prd)

    if prd == 0:
        cl_flag = True
        # print(model.predict(temp))

    if cl_flag and prd == 1:
        cl_flag = False
        summary = 0
        for x in prob:
            summary += max(x)
        acc = summary / len(prob)
        #print(acc)
        cl_counter += 1

    return cl_counter, acc

# def temp_ctr_ssc(op_keypoint):
#     global m_flag
#     global counter
#     global model  

#     prd = model.predict(op_keypoint)

#     if prd == 1:
#         m_flag = True
#         # print(model.predict(temp))

#     if m_flag and prd == 2:
#         m_flag = False
#         counter += 1

#     return counter


# def ctr_ssc(prd):
#     global m_flag
#     global counter

#     if prd == 26:
#         m_flag = True
#         # print(model.predict(temp))

#     if m_flag and prd == 14:
#         flm_flagag = False
#         counter += 1
#         print("count!", counter)


# def ctr_gm(prd):
#     global m_flag
#     global counter

#     if prd == 1:
#         m_flag = True
#         # print(model.predict(temp))

#     if m_flag and prd == 7:
#         m_flag = False
#         counter += 1
#         print("count!", counter)


# def ctr_cl(prd):
#     global m_flag
#     global counter
#     if prd == 1:
#         m_flag = True
#         # print(model.predict(temp))

#     if m_flag and prd == 2:
#         m_flag = False
#         counter += 1
#         print("count!", counter)

#     return counter


# # For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_pose.Pose(
#         min_detection_confidence=0.5,
#         min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         success, image = cap.read()
#         if not success:
#             print("Ignoring empty camera frame.")
#             # If loading a video, use 'break' instead of 'continue'.
#             continue

#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = pose.process(image)

#         # Draw the pose annotation on the image.
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         if results.pose_landmarks:
#             op_keypoint = [results.pose_landmarks.landmark[0].x,  # <<OpenPose기준>> 0번값 Nose
#                            results.pose_landmarks.landmark[2].x,  # 1번값 Left Eye
#                            results.pose_landmarks.landmark[5].x,  # 2번값 Right Eye
#                            results.pose_landmarks.landmark[7].x,  # 3번값 Left Ear
#                            results.pose_landmarks.landmark[8].x,  # 4번값 Right Ear
#                            results.pose_landmarks.landmark[11].x,  # 5번값 Left Shoulder
#                            results.pose_landmarks.landmark[12].x,  # 6번값 Right Shoulder
#                            results.pose_landmarks.landmark[13].x,  # 7번값 Left Elbow
#                            results.pose_landmarks.landmark[14].x,  # 8번값 Right Elbow
#                            results.pose_landmarks.landmark[15].x,  # 9번값 Left Wrist
#                            results.pose_landmarks.landmark[16].x,  # 10번값 Right Wrist
#                            results.pose_landmarks.landmark[23].x,  # 11번값 Left Hip
#                            results.pose_landmarks.landmark[24].x,  # 12번값 Right Hip
#                            results.pose_landmarks.landmark[25].x,  # 13번값 Left Knee
#                            results.pose_landmarks.landmark[26].x,  # 14번값 Right Knee
#                            results.pose_landmarks.landmark[27].x,  # 15번값 Left Ankle
#                            results.pose_landmarks.landmark[28].x,  # 16번값 Right Ankle
#                            0,  # 17번값 Neck
#                            0,  # 18번값 Left Palm -
#                            0,  # 19번값 Right Palm -
#                            0,  # 20번값 Back ?
#                            0,  # 21번값 Waist ?
#                            results.pose_landmarks.landmark[31].x,  # 22번값 Left Foot
#                            results.pose_landmarks.landmark[32].x,  # 23번값 Right Foot

#                            results.pose_landmarks.landmark[0].y,  # <<OpenPose기준>> 24번값 Nose
#                            results.pose_landmarks.landmark[2].y,  # 25번값 Left Eye
#                            results.pose_landmarks.landmark[5].y,  # 26번값 Right Eye
#                            results.pose_landmarks.landmark[7].y,  # 27번값 Left Ear
#                            results.pose_landmarks.landmark[8].y,  # 28번값 Right Ear
#                            results.pose_landmarks.landmark[11].y,  # 29번값 Left Shoulder
#                            results.pose_landmarks.landmark[12].y,  # 30번값 Right Shoulder
#                            results.pose_landmarks.landmark[13].y,  # 31번값 Left Elbow
#                            results.pose_landmarks.landmark[14].y,  # 32번값 Right Elbow
#                            results.pose_landmarks.landmark[15].y,  # 33번값 Left Wrist
#                            results.pose_landmarks.landmark[16].y,  # 34번값 Right Wrist
#                            results.pose_landmarks.landmark[23].y,  # 35번값 Left Hip
#                            results.pose_landmarks.landmark[24].y,  # 36번값 Right Hip
#                            results.pose_landmarks.landmark[25].y,  # 37번값 Left Knee
#                            results.pose_landmarks.landmark[26].y,  # 38번값 Right Knee
#                            results.pose_landmarks.landmark[27].y,  # 39번값 Left Ankle
#                            results.pose_landmarks.landmark[28].y,  # 40번값 Right Ankle
#                            0,  # 41번값 Neck
#                            0,  # 42번값 Left Palm -
#                            0,  # 43번값 Right Palm -
#                            0,  # 44번값 Back ?
#                            0,  # 45번값 Waist ?
#                            results.pose_landmarks.landmark[31].y,  # 46번값 Left Foot
#                            results.pose_landmarks.landmark[32].y]  # 47번값 Right Foot
#             # Neck
#             op_keypoint[17] = (results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x) / 2
#             op_keypoint[41] = (results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y) / 2

#             # Left Palm
#             op_keypoint[18] = (results.pose_landmarks.landmark[20].x + results.pose_landmarks.landmark[18].x +
#                                results.pose_landmarks.landmark[16].x) / 3
#             op_keypoint[42] = (results.pose_landmarks.landmark[20].y + results.pose_landmarks.landmark[18].y +
#                                results.pose_landmarks.landmark[16].y) / 3
#             # Right Palm
#             op_keypoint[19] = (results.pose_landmarks.landmark[19].x + results.pose_landmarks.landmark[17].x +
#                                results.pose_landmarks.landmark[15].x) / 3
#             op_keypoint[43] = (results.pose_landmarks.landmark[19].y + results.pose_landmarks.landmark[17].y +
#                                results.pose_landmarks.landmark[15].y) / 3
#             # Back
#             tmpx = (op_keypoint[17] - (
#                     (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x) / 2)) / 3
#             tmpy = (op_keypoint[41] - (
#                     (results.pose_landmarks.landmark[23].y + results.pose_landmarks.landmark[24].y) / 2)) / 3

#             op_keypoint[20] = op_keypoint[17] + tmpx
#             op_keypoint[44] = op_keypoint[41] + tmpy

#             # Waist
#             op_keypoint[21] = op_keypoint[17] + (tmpx * 2)
#             op_keypoint[45] = op_keypoint[41] + (tmpy * 2)

#         # # op_keypoint를 데이터프레임으로 바꾸자~~
#         temp = pd.DataFrame(np.array(op_keypoint), index=idx).T
#         # if model.predict(temp) > 20:
#         #     flag = True
#         # else:
#         #     flag = False
#         #
#         # print("good!" if flag else "")

#         # print('count' if model.predict(temp) == 1 else '')

#         # if model.predict(temp) == 26:
#         #     flag = True
#         #     # print(model.predict(temp))
#         #
#         # if flag and model.predict(temp) == 14:
#         #     flag = False
#         #     counter += 1
#         #     print("count!", counter)

#         # print(model.predict(temp))

#         # ctr_ssc(model.predict(temp))
#         # ctr_cl(model.predict(temp))
#         # ctr_gm(model.predict(temp))
        
#         # 각 변수의 확률 출력
#         # prob = model.predict_proba(temp)
#         # print(prob)
        
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#         # Flip the image horizontally for a selfie-view display.
#         cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#         if cv2.waitKey(5) & 0xFF == 27:
#             break

# cap.release()
