import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from PIL import Image
import cv2
import torch
import math 
import function.rotate as rotate
from IPython.display import display
import function.helper as helper
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


img_path = "test_image/12.jpg"

# load model
yolo_LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/lp_vn_det_v5s.pt', force_reload=True)
yolo_license_plate = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/lp_vn_ocr_yolov5s_final.pt', force_reload=True)
yolo_license_plate.conf = 0.80

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
        crop_img = helper.crop_expanded_plate(plate_xyxy=(x1, y1, x2, y2), img=img, expand_ratio=0.15)
        cv2.rectangle(img, (x1,y1), (x2,y2), color = (0,0,225), thickness = 1)
        cv2.imwrite("crop.jpg", crop_img)
        lp = ""
        for cc in range(0,2):
            for ct in range(0,2):
                lp = helper.read_plate(yolo_license_plate, rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    helper.draw_text(img=img, text=lp, pos=(x1, y1),  font_thickness=2, text_color=(0,255,0))
                    flag = 1
                    break
            if flag == 1:
                break
cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()