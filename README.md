# Traffic-Violation-Detection-System
=======
# VN License Plate Recognition

## Installation
- this project using python==3.8.20
```bash
  # install env and libraries using conda
  conda create --name env --file requirements.txt
```

- **Pretrained model** provided in ./model folder in this repo 

- Yolov5 old version is available in project folder

## Run License Plate Recognition

```bash
  # run inference on webcam
  python webcam.py 

  # run inference on image
  python image.py -i test_image/3.jpg
```

## Result
![Demo 1](result/test1.jpg)

![Demo 2](result/test2.jpg)
