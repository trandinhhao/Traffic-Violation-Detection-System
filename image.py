from PIL import Image  # Importing the PIL library for image processing
import cv2  # Importing OpenCV for image processing
import torch  # Importing PyTorch for deep learning
import math  # Importing math library
import function.utils_rotate as utils_rotate  # Importing custom rotation utilities
from IPython.display import display  # Importing display function from IPython
import os  # Importing os library for file operations
import time  # Importing time library
import argparse  # Importing argparse for command-line argument parsing
import function.helper as helper  # Importing custom helper functions

# Setting up argument parser for command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to input image')
args = ap.parse_args()

# Loading YOLO models for license plate detection and OCR
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.6  # Setting confidence threshold for OCR model

# Reading the input image
img = cv2.imread(args.image)
# Detecting license plates in the image
plates = yolo_LP_detect(img, size=640)

# Converting detection results to a list
list_plates = plates.pandas().xyxy[0].values.tolist()
list_read_plates = set()  # Set to store read license plates

# If no plates are detected, attempt to read the plate directly
if len(list_plates) == 0:
    lp = helper.read_plate(yolo_license_plate, img)
    if lp != "unknown":
        # Annotate the image with the detected license plate
        cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        list_read_plates.add(lp)
else:
    # Iterate over detected plates
    for plate in list_plates:
        flag = 0
        x = int(plate[0])  # xmin
        y = int(plate[1])  # ymin
        w = int(plate[2] - plate[0])  # xmax - xmin
        h = int(plate[3] - plate[1])  # ymax - ymin  
        crop_img = img[y:y+h, x:x+w]  # Crop the detected plate from the image
        # Draw a rectangle around the detected plate
        cv2.rectangle(img, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
        cv2.imwrite("crop.jpg", crop_img)  # Save the cropped image
        rc_image = cv2.imread("crop.jpg")  # Read the cropped image
        lp = ""
        # Try different deskewing configurations to read the plate
        for cc in range(0, 2):
            for ct in range(0, 2):
                lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    # Annotate the image with the detected license plate
                    cv2.putText(img, lp, (int(plate[0]), int(plate[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    flag = 1
                    break
            if flag == 1:
                break

# Display the final image with annotations
cv2.imshow('frame', img)
cv2.waitKey()
cv2.destroyAllWindows()