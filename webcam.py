from PIL import Image
import cv2
import torch
import math
import function.utils_rotate as utils_rotate
from IPython.display import display
import os
import time
import argparse
import function.helper as helper
import csv
from datetime import datetime

# Load models
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector_nano_61.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr_nano_62.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60

# CSV file paths
license_plate_file = "license_plate.csv"
valid_plate_file = "valid_plate.csv"

# Video stream setup
vid = cv2.VideoCapture("./test_video/v1.mp4")
# vid = cv2.VideoCapture(0)

start_time = time.time()
plate_detection_duration = 30  # 30 seconds for detection
cycle_duration = 60
prev_frame_time = 0
new_frame_time = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    ret, frame = vid.read()
    if not ret:
        break

    if elapsed_time % cycle_duration < plate_detection_duration:
        # License plate detection (First 30 seconds)
        plates = yolo_LP_detect(frame, size=640)
        list_plates = plates.pandas().xyxy[0].values.tolist()
        list_read_plates = set()
        for plate in list_plates:
            flag = 0
            x = int(plate[0])  # xmin
            y = int(plate[1])  # ymin
            w = int(plate[2] - plate[0])  # xmax - xmin
            h = int(plate[3] - plate[1])  # ymax - ymin
            crop_img = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
            cv2.imwrite("crop_plate.jpg", crop_img)
            rc_image = cv2.imread("crop_plate.jpg")
            lp = ""
            for cc in range(0, 2):
                for ct in range(0, 2):
                    lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        cv2.putText(frame, lp, (int(plate[0]), int(plate[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        flag = 1
                        break
                if flag == 1:
                    break
        
        # Save detected plates to CSV
        with open(license_plate_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for lp in list_read_plates:
                writer.writerow([lp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    else:
        # Data processing (Next 30 seconds)
        # Read from license_plate.csv, filter data, and save to valid_plate.csv
        try:
            with open(license_plate_file, mode='r') as infile, open(valid_plate_file, mode='a', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                for row in reader:
                    # Apply filtering logic here
                    
                    if not helper.check_valid_plate(row[0]): continue
                    writer.writerow(row)
            
            # Clear the license_plate.csv by overwriting it with nothing
            with open(license_plate_file, mode='w', newline='') as infile:
                pass  # This will empty the file
        
        except FileNotFoundError:
            print("CSV file not found, skipping processing...")

    # Calculate and display FPS
    new_frame_time = time.time()
    fps = 0
    if (new_frame_time-prev_frame_time)!=0: fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
vid.release()
cv2.destroyAllWindows()
