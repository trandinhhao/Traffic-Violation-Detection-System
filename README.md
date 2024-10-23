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
- API and Script using Nodejs 20.18.0
```bash
  # installs fnm (Fast Node Manager)
  winget install Schniz.fnm
  
  # configure fnm environment
  fnm env --use-on-cd | Out-String | Invoke-Expression
  
  # download and install Node.js
  fnm use --install-if-missing 20
  
  # verifies the right Node.js version is in the environment
  node -v # should print `v20.18.0`
  
  # verifies the right npm version is in the environment
  npm -v # should print `10.8.2`

  # Sets up the fnm environment to automatically switch Node.js versions when changing directories
  fnm env --use-on-cd | Out-String | Invoke-Expression

  # Navigates to the project directory where the traffic violation project is located
  cd traffic-violation-project

```

## Run License Plate Recognition

```bash
  # run inference on webcam
  python webcam.py 

  # run inference on image
  python image.py -i test_image/3.jpg

  # Run import script
  node import.js  # This will import data from the CSV file to the database.

  # Start the server
  node server.js  # This will start the API server.

  # Test the API
  You can test whether a license plate exists in the database by sending a GET request to the following endpoint:
  http://localhost:3000/api/violations/<licensePlate>
  For example: http://localhost:3000/api/violations/34A8-0963



```

## Result
![Demo 1](result/test1.jpg)

![Demo 2](result/test2.jpg)
