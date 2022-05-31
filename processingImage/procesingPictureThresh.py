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

img = cv.imread('processingImage\Image1.jpg', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[270:330,:]

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)



height = img.shape[0]
width = img.shape[1]

print('Chieu rong cua buc hinh', width)
print('Chieu dai cua buc hinh', height)


thresh = 70
b_image = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)[1]
cv.circle(img,(300,30),1,(255,0,255),10)
cv.line(img,(20,10),(20,20),(255,0,0),1)

cv.imshow('Onghan1', b_image)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()