import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from PIL import Image
import cv2
import torch
import math 
import function.rotate as rotate
from IPython.display import display
import function.helper as helper

img_path = ""

# load detect model
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')

img = cv2.imread(img_path)
plates = yolo_LP_detect(img, size=640)
print("Checkpoint")
list_plates = plates.pandas().xyxy[0].values.tolist()
list_read_plates = set()
if len(list_plates) == 0:
    lp = helper.read_plate_ppocr(img)
    if lp != "unknown":
        cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        list_read_plates.add(lp)
else:
    for plate in list_plates:
        flag = 0
        x1 = int(plate[0]) 
        y1 = int(plate[1]) 
        x2 = int(plate[2]) 
        y2 = int(plate[3]) 
        crop_img = img[y1:y2, x1:x2]
        cv2.rectangle(img, (x1,y1), (x2,y2), color = (0,0,225), thickness = 2)
        cv2.imwrite("crop_plate.jpg", crop_img)
        # rc_image = cv2.imread("crop_plate.jpg")
        lp = ""
        for cc in range(0,2):
            for ct in range(0,2):
                crop_img_ver = rotate.deskew(crop_img, cc, ct)
                cv2.imwrite("crop_plate"+str(cc)+str(ct)+".jpg", crop_img_ver)
                # lp = helper.read_plate_ppocr("crop_plate.jpg")
                lp = helper.read_plate_ppocr(crop_img)
                if lp != "unknown":
                    list_read_plates.add(lp)
                    cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    flag = 1
                    break
            if flag == 1:
                break
cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()