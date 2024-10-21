# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run a Flask REST API exposing a YOLOv5s model
"""

import argparse
import io

import torch
from flask import Flask, request
from PIL import Image

import os
import pandas as pd
import shutil
import cv2
import json
import tensorflow as tf
from tensorflow.keras.models import Model
from skimage import transform
import numpy as np
import requests
from datetime import datetime

app = Flask(__name__)
global model 


DETECTION_URL = "/classification"

def classification(filename):
    target_names = ['fire', 'normal', 'war']
    # model = tf.keras.models.load_model('C:/Users/Admin/Downloads/my_model_xception_12_5.h5')
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (240, 240, 3))
    np_image = np.expand_dims(np_image, axis=0)
    arr = model.predict(np_image)[0]
    return target_names[np.around(arr).argmax()]
    

@app.route(DETECTION_URL, methods=["POST", "GET"])
def predict():
    if request.method == "GET":
        file_url = request.args.to_dict()['img_url']
        # data = request.args
        # print(type(data))
        # print(data.to_dict())
        
        # Temp = data['Temp']
        # request.form
        # f = open('C:/Users/Admin/Desktop/yolov5/utils/flask_rest_api/temp.jpg','wb')
        # f.write(requests.get(file_url).content)
        # f.close()
        # im_bytes = im_file.read()
        # im = Image.open(requests.get(file_url, stream=True).raw)
        response = requests.get(file_url)
        im = Image.open(io.BytesIO(response.content))
        
        # classification model
        target_names = ['fire', 'normal', 'war']
        # np_image = Image.open(im_file)
        np_image = np.array(im).astype('float32')/255
        np_image = transform.resize(np_image, (240, 240, 3))
        np_image = np.expand_dims(np_image, axis=0)
        arr = model.predict(np_image)[0]
        lab = target_names[np.around(arr).argmax()]

        label_list = "Classes: " + lab
        results = model_yolo(im, size=640)  # reduce size=320 for faster inference

        yolo_l = results.pandas().xyxy[0].values
        yolo_labels = set()
        for item in yolo_l:
            yolo_labels.add(item[6])
        for i in yolo_labels:
            label_list += ", " + i
        # fin = lab + yolo_lab
        return label_list
        # return file_url

    elif request.method == "POST":
        if request.files.get("image"):
            # Method 1
            # with request.files["image"] as f:
            #     im = Image.open(io.BytesIO(f.read()))

            # Method 2
            im_file = request.files["image"]
            im_bytes = im_file.read()
            im = Image.open(io.BytesIO(im_bytes))

            # classification model
            target_names = ['fire', 'normal', 'war']
            np_image = Image.open(im_file)
            Image.save(datetime.now().strftime("%H:%M:%S"))
            print(type(np_image))
            np_image = np.array(np_image).astype('float32')/255
            np_image = transform.resize(np_image, (240, 240, 3))
            np_image = np.expand_dims(np_image, axis=0)
            arr = model.predict(np_image)[0]
            lab = target_names[np.around(arr).argmax()]

            label_list = "Classes: " + lab
            results = model_yolo(im, size=640)  # reduce size=320 for faster inference

            yolo_l = results.pandas().xyxy[0].values
            yolo_labels = set()
            for item in yolo_l:
                yolo_labels.add(item[6])
            for i in yolo_labels:
                label_list += ", " + i
            # fin = lab + yolo_lab
            return label_list
    else:
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    opt = parser.parse_args()

    # Fix known issue urllib.error.HTTPError 403: rate limit exceeded https://github.com/ultralytics/yolov5/pull/7210
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

    model = tf.keras.models.load_model('C:/Users/Admin/Downloads/my_model_xception_13_5.h5')
    # model_yolo = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    model_yolo = torch.hub.load('C:/Users/Admin/Desktop/yolov5', 'custom', path='C:/Users/Admin/Desktop/yolov5/best_large.pt', force_reload=True, source='local')
    model_yolo.to('cpu') 
    app.run(host="0.0.0.0", port=opt.port)  # debug=True causes Restarting with stat
