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

img = cv.imread('image\imageBeauty\image_22.png', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[270:330,:]

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# plt.hist(gray.ravel(),256,[0,256]); plt.show()

roi = gray[0:15,0:15]
# thresh = np.mean(roi)
# print(thresh)
thresh = 45
height = img.shape[0]
width = img.shape[1]

print('Chieu rong cua buc hinh', width)
print('Chieu dai cua buc hinh', height)

b_image = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY_INV)[1]

kenel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
out_1 = cv.morphologyEx(b_image,cv.MORPH_CLOSE,kenel,iterations=1)

contour, hierachy = cv.findContours(b_image,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
for c in contour:
    if cv.contourArea(c) > 10:
        area = cv.contourArea(c)
        print(area)
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(img,[box],0,(0,0,255),2)
    
cv.line(img,(300,0),(300,60),(255,0,0),2)

cv.imshow('thresholdn', b_image)
cv.imshow('Threshol ong han', out_1)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()