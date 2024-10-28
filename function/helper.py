import math
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from paddleocr import PaddleOCR
import numpy as np
import re

def check_valid_plate(plate: str) -> bool:
    parts = plate.split('-')
    if len(parts) != 2 or (len(parts[0])!=3 and len(parts[0])!=4) or (len(parts[1])!=4 and len(parts[1])!=5):
        return False
    unknown_plate = ["13", "42", "44", "45", "46", "87", "91", "96"]
    if (parts[0][0].isalpha() or parts[0][1].isalpha() or parts[0][2].isnumeric()): return False
    for char in parts[1]:
        if (char.isalpha()): return False

    if parts[0] in unknown_plate: return False
    return True
    


ocr = PaddleOCR(lang="en")

def read_plate_ppocr(plate_path) -> str:
    result = ocr.ocr(plate_path)[0]
    if (result==None): return "unknown"
    print(result)
    LP_type = str(len(result))
    text = ""
    cnt = 0
    # if (LP_type != "1" or LP_type != "2"): return "unknown"
    for r in result:
        print("OCR"+str(cnt), r)
        scores = r[1][1]
        if np.isnan(scores):
            scores = 0
        else:
            scores = int(scores * 100)
        if scores > 80:
            if cnt==0: text += r[1][0]
            else: text += "-" + r[1][0]  
            cnt += 1
        else:
            return "unknown"
        
    # pattern = re.compile('[\W]')
    # text = pattern.sub('', text)
    text = text.replace("???", "")
    text = text.replace("O", "0")
    # if cnt!=len(result): return "unknown"
    return str(text)