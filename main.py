import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
# Load COCO class names
with open("coco1.txt", "r") as f:
    class_names = f.read().splitlines()

# Load the YOLOv8 model
model = YOLO("best.pt")

# Open the video file (use video file or webcam, here using webcam)
cap = cv2.VideoCapture(cv2.CAP_V4L2)
checkObject = []
count = 0

while True:
    frame= picam2.capture_array()
    
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.flip(frame,-1)

#    frame = cv2.resize(frame, (1020, 500))
    
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True, imgsz=256, verbose=False)
    checkObject = []
    # Check if there are any boxes in the results
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
        track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score
       
        for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
            c = class_names[class_id]
            x1, y1, x2, y2 = box
            centerX,centerY = (x1+abs(x1-x2)//2,y1+abs(y1-y2)//2)
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(frame,(centerX,centerY),5,(255,0,0),-1,cv2.LINE_AA)
            cvzone.putTextRect(frame,f'{track_id}',(x1,y2),1,1)
            cvzone.putTextRect(frame,f'{c} | X:{centerX},Y:{centerY}',(x1,y1),1,1)
            checkObject.append({"pos":(centerX,centerY),"class":c})
    print("-"*100,checkObject)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
       break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

