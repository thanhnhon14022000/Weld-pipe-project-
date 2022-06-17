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

img = cv.imread('image\imageBeauty\image_30.png', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[290:310,200:400]

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# plt.hist(gray.ravel(),256,[0,256]); plt.show()

roi = gray[0:15,0:15]
thresh_roi = np.mean(roi)-10
print(thresh_roi)
# print(thresh)
thresh = 60
height = img.shape[0]
width = img.shape[1]

print('Chieu rong cua buc hinh', width)
print('Chieu dai cua buc hinh', height)

b_image = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY_INV)[1]

lines = cv.HoughLinesP(b_image, 1, np.pi/180, 10, minLineLength=5, maxLineGap=8)

for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1,y1),(x2,y2),(0,255,0),1)
print(lines)
cv.line(img,(100,0),(100,20),(255,0,0),2)

cv.imshow('Threshol ong han', b_image)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()