# Import mudules
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Dimension constant
alpha = 5
beta = 0
sizeH = 600
SizeW = 600
centerimg = (sizeH/2, SizeW/2)
dimensionDrop = 20
# Load Image

img = cv.imread('processingImage\Image7.jpg', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[290:310,200:400]

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_gray_ct = cv.addWeighted(img_gray, 4, np.zeros(
        img_gray.shape, img_gray.dtype), 0, beta)

blur_img = cv.blur(img_gray_ct, (5, 5))
binary_img = cv.adaptiveThreshold(blur_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 2)
binary_img = cv.erode(binary_img, None, iterations=2)
skeleton_img = cv.ximgproc.thinning(binary_img, 0)
cv.imshow('skeleton_img', skeleton_img)
cv.imshow('binary_img', img)

cv.waitKey(0)
cv.destroyAllWindows()