from re import L
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from imutils import perspective
from scipy.spatial import distance as dist

# function returns current size of pipe
def dimensition(size): 
    global scale
    #coefficient that returns the true size of the pipe
    scale = 10
    size = size / scale
    if size <= 25:
        size = 21
    if size > 25 and size < 30:
        size = 27
    if size >=30 and size < 38:
        size = 34
    if size >= 38 and size < 45:
        size = 42
    if size >=45 and size < 54:
        size = 48
    if size >=54:
        size = 60
    return size

# Dimension constant
sizeH = 600
SizeW = 600
centerimg = (sizeH/2, SizeW/2)
dimensionDrop = 20

# Load Image
img = cv.imread('image\imageBeauty\image_30.png', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

canny = cv.Canny(img_gray,20,100)

kenel = cv.getStructuringElement(cv.MORPH_RECT,(9,9))
out_1 = cv.morphologyEx(canny,cv.MORPH_CLOSE,kenel,iterations=1)

contour, hierachy = cv.findContours(out_1,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) / 2, (ptA[1] + ptB[1]) / 2)

for c in contour:
    if cv.contourArea(c) < 3000:
        continue
    box = cv.minAreaRect(c)
    box = cv.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)        
    cv.drawContours(img,[box.astype("int")], -1, (0, 255, 0), 2)
    (A, B, C, D) = box
    (Ex,Ey) = midpoint(A,B)
    (Fx,Fy) = midpoint(B,C)
    (Gx,Gy) = midpoint(C,D)
    (Hx,Hy) = midpoint(D,A)
    W = dist.euclidean((Hx,Hy),(Fx,Fy)) 
    H = dist.euclidean((Ex, Ey),(Gx, Gy))
    P = 0.027
    Wr = round(W*P,1)*10
    Hr = round(H*P,1)*10
    print('Kich thuoc cua ong: ', Hr)
    a = dimensition(Hr)
    print('Kich thuoc cua ong sau khi scale',a)
    cv.putText(img, "{:.1f} mm".format(Hr), (int(Hx - 15), int(Hy)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
    cv.putText(img, "{:.1f} mm".format(Wr), (int(Ex), int(Ey-10)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
print(contour)
cv.imshow('Hinhanhthuc', canny)
cv.imshow('Onghan', img)
cv.waitKey(0)
cv.destroyAllWindows()