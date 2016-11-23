import cv2
import numpy as np
import time
import os

cwd = os.getcwd()
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(cwd+'/calib/line-scan.avi', fourcc, 12, (1280, 720))       #4608x2592

for i in range(0, 1280, 10):
    img = np.zeros((1280, 720))
    img[i, :] = 255
    cv2.imshow('preview', img)
    #rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #out.write(img)
