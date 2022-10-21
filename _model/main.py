import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

op_keypoint = []

# For webcam input:
# cap = cv2.VideoCapture('posevideo1.mp4')
cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    flag = False

    while cap.isOpened():   # 카메라가 열려있는 동안 루프
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue    # video일 경우 break`

        image.flags.writeable = False    # 성능 향상을 위해 이미지 쓰기불가시켜 참조로 전달
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)   # pose 검출

        # COCO17개로 바꾸기

        image.flags.writeable = True    # 다시 쓰기 가능으로 변경
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        min_i = 1.0

        if results.pose_landmarks:
            op_keypoint = [results.pose_landmarks.landmark[0],  # <<OpenPose기준>> 0번값
                           results.pose_landmarks.landmark[11],  # 1번값, 11과 12의 평균
                           results.pose_landmarks.landmark[12],  # 2번값
                           results.pose_landmarks.landmark[14],  # 3번값
                           results.pose_landmarks.landmark[16],  # 4번값
                           results.pose_landmarks.landmark[11],  # 5번값
                           results.pose_landmarks.landmark[13],  # 6번값
                           results.pose_landmarks.landmark[15],  # 7번값
                           results.pose_landmarks.landmark[24],  # 8번값
                           results.pose_landmarks.landmark[26],  # 9번값
                           results.pose_landmarks.landmark[28],  # 10번값
                           results.pose_landmarks.landmark[23],  # 11번값
                           results.pose_landmarks.landmark[25],  # 12번값
                           results.pose_landmarks.landmark[27],  # 13번값
                           results.pose_landmarks.landmark[5],  # 14번값
                           results.pose_landmarks.landmark[2],  # 15번값
                           results.pose_landmarks.landmark[8],  # 16번값
                           results.pose_landmarks.landmark[7]]  # 17번값
            op_keypoint[1].x = (results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x) / 2
            op_keypoint[1].y = (results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y) / 2
            op_keypoint[1].z = (results.pose_landmarks.landmark[11].z + results.pose_landmarks.landmark[12].z) / 2
            op_keypoint[1].visibility = (results.pose_landmarks.landmark[11].visibility +
                                         results.pose_landmarks.landmark[12].visibility) / 2

            for i in results.pose_landmarks.landmark:
                #print(i.visibility)
                min_i = min(min_i, i.visibility)

            if min_i > 0.6:  # 0.5 ~ 0.6사이가 좋을듯
                flag = True
                # 내용 추가. keypoint의 좌표를 dataframe으로 만듬

                keypoint_list = {}
                for kp in op_keypoint:
                    for i in range(18):
                        keypoint_list[i] = {'x': kp[i].x, 'y': kp[i].y}
                        # mediapipe 좌표를 python에서 다룰 수 있게 바꿔야함
                        # TypeError: 'NormalizedLandmark' object is not subscriptable

            if flag:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            '''
            for pose in results.pose_landmarks :

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            '''

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            print(keypoint_list)
            break
cap.release()


