# Import mudules
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# Dimension constant
sizeH = 600
SizeW = 600
centerimg = (sizeH/2, SizeW/2)
dimensionDrop = 20
# Load Image

img = cv.imread('processingImage\hinh2.jpg', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[270:330,:]

hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

low_thes = (0,0,0)
high_thes = (360,255,60)

line = cv.inRange(hsv,low_thes,high_thes)

kenel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
out_1 = cv.morphologyEx(line,cv.MORPH_CLOSE,kenel,iterations=1)


cv.imshow('Threshol ong han', out_1)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()