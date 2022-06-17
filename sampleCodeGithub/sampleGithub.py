# Import mudules
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Dimension constant
alpha = 4
beta = 0
sizeH = 600
SizeW = 600
center = int(sizeH / 2)
dimensionDrop = 20
leftframe = 290
rightframe = 302

# Load Image
img = cv.imread('E:\Processing Image\image\imageBeauty\image_19.png', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[270:330,:]

#Camera center line and center frame
cv.line(img,(center,0),(center,90),(0,255,0),1)
cv.rectangle(img, (leftframe, 0), (rightframe,60), (0,0,255),1)

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

img_gray_ct = cv.addWeighted(img_gray, alpha, np.zeros(img_gray.shape, img_gray.dtype), 0, beta)

blur_img = cv.blur(img_gray_ct, (7,7))
binary_img = cv.adaptiveThreshold(blur_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 2)
binary_img = cv.erode(binary_img, None, iterations=2)
skeleton_img = cv.ximgproc.thinning(binary_img, 0)

lines = cv.HoughLinesP(skeleton_img, 1, np.pi/180, 20, minLineLength=30, maxLineGap=10)

for line in lines:
    x1,y1,x2,y2 = line[0]
    if(abs(x1-x2)) < 5:
        weld = line[0]
        print(line)
        cv.line(img,(x1,y1),(x2,y2),(255,0,0),1)

if weld[0] > leftframe and weld[0] < rightframe:
        print('Mối hàn đã vào tâm') 


cv.imshow('binary_img', binary_img)
cv.imshow('img', img)
cv.imshow('img_gray_ct img_gray_ct ', img_gray_ct)
cv.imshow('skeleton_img ', skeleton_img)
cv.waitKey(0)
cv.destroyAllWindows()
