import cv2 as cv
import numpy as np

sizeH = 600
SizeW = 600


img = cv.imread('processingImage\Image2.jpg', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img = img[280:320,:]
# img = cv.GaussianBlur(img,(3,3),0)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

canny = cv.Canny(gray,300,350)

lines = cv.HoughLinesP(canny, 1, np.pi/180, 3, minLineLength=15, maxLineGap=3)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1,y1),(x2,y2),(0,255,0),1)
    print(line)


cv.line(img,(300,0),(300,60),(255,0,0),1)
cv.imshow('Hinh Canny', canny)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()