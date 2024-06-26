import cv2
import torch
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
from KaKao_Talk_friend import SEND_MESSAGE_TO_FRIEND
from upload_image import UPLOAD_IMAGE
from KaKao_Talk_me import SEND_MESSAGE_TO_ME
import datetime
import asyncio

# 이미지 저장 경로
IMAGE_SAVE_PATH = '/home/student/Desktop/project/Project/detected_object'

# YOLOv5 디렉토리 설정
YOLOv5_DIR = '/home/student/Desktop/project/yolov5'  # 로컬에 저장된 YOLOv5 경로

# 사용자 정의 모델 경로 설정
MODEL_WEIGHTS = '/home/student/Desktop/project/yolov5/runs/train/project0606_12/weights/best.pt'  # 학습된 모델 가중치 경로

# 모델 로드
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load(YOLOv5_DIR, 'custom', path=MODEL_WEIGHTS, source='local')
model = model.to(device)
model.eval()

video_path = '/home/student/Desktop/project/dataset/old_data/new_test/test_0604(1).mp4'

# 비디오 캡처 (웹캠: 0, 비디오 파일 경로)
cap = cv2.VideoCapture(video_path)  # 또는 'your_video.mp4'

frame_idx = 0
detection_count = 0

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(IMAGE_SAVE_PATH):
    os.makedirs(IMAGE_SAVE_PATH)

pr_detected = set()

# 클래스별 색상 정의
class_colors = {
    'bill': (255, 0, 0),
    'ring': (0, 255, 0),
    'watch': (0, 0, 255),
    # 필요한 다른 클래스들 추가
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 이미지 전처리
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(img)
    
    detected_objects = set()
    
    # 결과 후처리 및 표시
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if conf > 0.7:  # 신뢰도 필터링
            label = model.names[int(cls)]
            color = class_colors.get(label, (255, 255, 255))  # 클래스 색상 선택, 기본 색상은 흰색
            
            # 바운딩 박스 그리기
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            detected_objects.add(label)
    # 이미지 출력
    cv2.imshow('Camera Feed', frame)
    
    # 이전 검출 외, 새롭게 검출된 라벨
    new_detected = detected_objects - pr_detected
    
    if new_detected:   
        # 파일명 생성
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%m%d_%H%M%S")
        filename = os.path.join(IMAGE_SAVE_PATH, f'detected_{timestamp}.jpg')
                
        # 이미지 저장
        cv2.imwrite(filename, frame)
        print(f'New object detected: {new_detected}. Image saved as {filename}')
        UPLOAD_IMAGE(timestamp, filename)
        SEND_MESSAGE_TO_FRIEND(new_detected, timestamp)
        #SEND_MESSAGE_TO_ME(new_detected, timestamp)

        # 이전 감지 업데이트             
        pr_detected = detected_objects.copy()
               
    # 'q' 키를 누르면 종료
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    frame_idx += 1