import cv2 as cv
import numpy as np

sizeH = 600
SizeW = 600


img = cv.imread('processingImage\Image2.jpg', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[290:310,:]
# img = cv.GaussianBlur(img,(3,3),0)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


canny = cv.Canny(gray,250,350)
cv.imshow('Onghan', canny)
cv.waitKey(0)
cv.destroyAllWindows()