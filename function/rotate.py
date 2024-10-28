import numpy as np
import math
import cv2

# Function to enhance the contrast of an image using CLAHE (Contrast Limited Adaptive Histogram Equalization)
def changeContrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # Convert the image from BGR to LAB color space
    l_channel, a, b = cv2.split(lab)  # Split the LAB image into different channels
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))  # Create a CLAHE object
    cl = clahe.apply(l_channel)  # Apply CLAHE to the L-channel
    limg = cv2.merge((cl, a, b))  # Merge the CLAHE enhanced L-channel with the a and b channels
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)  # Convert the LAB image back to BGR color space
    return enhanced_img

# Function to rotate an image by a given angle
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)  # Get the center of the image
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)  # Get the rotation matrix
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)  # Apply the rotation
    return result

# Function to compute the skew angle of an image
def compute_skew(src_img, center_thres):
    if len(src_img.shape) == 3:
        h, w, _ = src_img.shape  # Get the height and width of the image
    elif len(src_img.shape) == 2:
        h, w = src_img.shape  # Get the height and width of the image
    else:
        print('unsupported image type')
        return 0.0

    img = cv2.medianBlur(src_img, 3)  # Apply median blur to the image
    edges = cv2.Canny(img, threshold1=30, threshold2=100, apertureSize=3, L2gradient=True)  # Detect edges using Canny edge detector
    lines = cv2.HoughLinesP(edges, 1, math.pi/180, 30, minLineLength=w / 1.5, maxLineGap=h/3.0)  # Detect lines using Hough Line Transform
    if lines is None:
        return 1

    min_line = 100
    min_line_pos = 0
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            center_point = [((x1 + x2) / 2), ((y1 + y2) / 2)]  # Calculate the center point of the line
            if center_thres == 1:
                if center_point[1] < 7:
                    continue
            if center_point[1] < min_line:
                min_line = center_point[1]
                min_line_pos = i

    angle = 0.0
    cnt = 0
    for x1, y1, x2, y2 in lines[min_line_pos]:
        ang = np.arctan2(y2 - y1, x2 - x1)  # Calculate the angle of the line
        if math.fabs(ang) <= 30:  # Exclude extreme rotations
            angle += ang
            cnt += 1
    if cnt == 0:
        return 0.0
    return (angle / cnt) * 180 / math.pi  # Return the average angle in degrees

# Function to deskew an image
def deskew(src_img, change_cons, center_thres):
    if change_cons == 1:
        return rotate_image(src_img, compute_skew(changeContrast(src_img), center_thres))  # Enhance contrast and then compute skew
    else:
        return rotate_image(src_img, compute_skew(src_img, center_thres))  # Directly compute skew