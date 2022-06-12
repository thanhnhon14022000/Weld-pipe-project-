from concurrent.futures import thread
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from imutils import perspective
from scipy.spatial import distance as dist
# Dimension constant
sizeH = 600
SizeW = 600
centerimg = (sizeH/2, SizeW/2)
dimensionDrop = 20
# Load Image

img = cv.imread('image\imageBeauty\image_1.png', cv.IMREAD_COLOR)
img = cv.resize(img, dsize = (sizeH,SizeW))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


roi = gray[0:600,100:300]

thresh = np.mean(roi)-30

# print(thresh)

b_image = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY_INV)[1]


contour, hierachy = cv.findContours(b_image,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

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
    Hr = round(H*P,1)*10 #Kich thuoc cua ong
    print('Kich thuoc cua ong: ', Hr)
    cv.putText(img, "{:.1f} mm".format(Hr), (int(Hx - 15), int(Hy)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
    cv.putText(img, "{:.1f} mm".format(Wr), (int(Ex), int(Ey-10)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
cv.imshow('Anh gray', gray)
cv.imshow('Kich thuoc', img)
cv.imshow('Onghan', roi)
cv.imshow('Hinhanhthuc', b_image)
cv.waitKey(0)
cv.destroyAllWindows()  