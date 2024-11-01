from PIL import Image
import cv2
import torch
import math 
import function.rotate as rotate
from IPython.display import display
import os
import time
import argparse
import function.helper as helper
import csv
from datetime import datetime

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# load model
yolo_LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/lp_vn_det_v5s.pt', force_reload=True)
yolo_license_plate = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/lp_vn_ocr_yolov5m.pt', force_reload=True)
yolo_license_plate.conf = 0.60

prev_frame_time = 0
new_frame_time = 0

# vid = cv2.VideoCapture(0)
vid = cv2.VideoCapture("D:/Videos/lp_video/v23.mp4")

while(True):
    ret, frame = vid.read()
    
    plates = yolo_LP_detect(frame, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    list_read_plates = set()
    for plate in list_plates:
        flag = 0
        x1 = int(plate[0]) 
        y1 = int(plate[1]) 
        x2 = int(plate[2]) 
        y2 = int(plate[3]) 
        crop_img = frame[y1:y2, x1:x2]
        cv2.rectangle(frame, (x1,y1), (x2,y2), color = (0,0,225), thickness = 2)
        cv2.imwrite("crop.jpg", crop_img)
        lp = ""
        for cc in range(0,2):
            for ct in range(0,2):
                lp = helper.read_plate(yolo_license_plate, rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    cv2.putText(frame, lp, (int(plate[0]), int(plate[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    flag = 1
                    break
            if flag == 1:
                break
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()