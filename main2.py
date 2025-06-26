import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
import random
import threading
# Picamera2 관련 코드 삭제
# picam2 = Picamera2()
# picam2.preview_configuration.main.size = (640,480)
# picam2.preview_configuration.main.format = "RGB888"
# picam2.preview_configuration.align()
# picam2.configure("preview")
# picam2.start()
# Load COCO class names

from stepmoter import StepMoter
from limitswitch import LimitSwitch
from flask import Flask,render_template,redirect

xmoter = StepMoter(14,15)
ymoter = StepMoter(25,8)
grap = StepMoter(23,24)

xmove=False
ymove=False

xleft = LimitSwitch(20)
xright = LimitSwitch(16)
yleft = LimitSwitch(21)
yright = LimitSwitch(12)

wantObject = "ss_grape"
camera_running = True

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/button1')
def button1():
    global wantObject
    wantObject = "ss_grape"
    return redirect('/')

@app.route('/button2')
def button2():
    global wantObject
    wantObject = "ss_strewberry"
    return redirect('/')

#@app.teardown_appcontext
#def cleanup(exception=None):
    #GPIO.cleanup()

def simpleMoter(entity:StepMoter,sensor:LimitSwitch,steps,delay,rotation=False):
    entity.TurnRotation(rotation)
    entity.Action(sensor,steps,delay)

def startpoint():
    while not xleft.digitalRead():
        simpleMoter(xmoter,xleft,20,0.05,True)
    while not yleft.digitalRead():
        simpleMoter(ymoter,yleft,20,0.05,True)

def serchpoint():
    simpleMoter(xmoter,xright,150,0.001)
    simpleMoter(ymoter,yright,150,0.001)

def camera_loop():
    global camera_running
    with open("coco1.txt", "r") as f:
        class_names = f.read().splitlines()

    # Load the YOLOv8 model
    model = YOLO("best.pt")

    # Open the video file (use video file or webcam, here using webcam)
    cap = cv2.VideoCapture(0)  # 0번 장치가 기본 웹캠입니다.
    checkObject = []
    count = 0

    serching = True
    startpoint()
    serchpoint()

    try:
        while camera_running:
            ret, frame = cap.read()  # 웹캠에서 프레임 읽기
            if not ret:
                print("웹캠에서 프레임을 읽을 수 없습니다.")
                break
            count += 1
            if count % 3 != 0:
                continue
            frame = cv2.flip(frame, -1)

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True, imgsz=256,verbose=False)
            checkObject = []
        # Check if there are any boxes in the results
            if results[0].boxes is not None and results[0].boxes.id is not None and not serching:
            # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
                boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
                class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
                track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
                confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score
           
                for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                    c = class_names[class_id]
                    x1, y1, x2, y2 = box
                    if c == wantObject:
                        print(f"find id:{wantObject} ")
                        centerX, centerY = (x1 + abs(x1 - x2) // 2, y1 + abs(y1 - y2) // 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (centerX, centerY), 5, (255, 0, 0), -1, cv2.LINE_AA)
                        cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
                        cvzone.putTextRect(frame, f'{c} | X:{centerX},Y:{centerY}', (x1, y1), 1, 1)
                        checkObject.append({"pos": (centerX, centerY), "class": c})
                    else:
                        print("not found")
            print("-" * 100)
            serching = True

            if serching:
                if len(checkObject) <=0:
                    serching = False
                else:
                    select = random.choice(checkObject)
                    print(select)
                    startpoint()
                    for _ in range(select["pos"][0]//12):
                        simpleMoter(xmoter,xright,30,0.05)
                    for _ in range(select["pos"][1]//14):
                        simpleMoter(ymoter,yright,30,0.05)
                    #simpleMoter(grap,450,0.01,True)
            startpoint()
            cv2.imshow("RGB", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        pass

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 카메라 스레드 시작
    camera_thread = threading.Thread(target=camera_loop)
    camera_thread.daemon = True  # 메인 프로그램 종료시 함께 종료
    camera_thread.start()
    
    # Flask 서버 시작
    app.run(port=3000, host="0.0.0.0")

