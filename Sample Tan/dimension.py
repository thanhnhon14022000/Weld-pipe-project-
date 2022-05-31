import cv2 as cv
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective

# Load hình ảnh dưới dạng ảnh màu
img = cv.imread('sach.jpg',cv.IMREAD_COLOR)
img = cv.resize(img, dsize=(600, 600))

# Chuyển đổi ảnh màu sang ảnh xám
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#sử dụng bộ lọc canny
canny = cv.Canny(gray,90,150)
canny1 = canny

#Xử lý lọc nhiễu
kernel = cv.getStructuringElement(cv.MORPH_RECT,(3,3))
canny = cv.morphologyEx(canny,cv.MORPH_CLOSE, kernel, iterations=1)

# Tìm các đường contour
contour, hierachy = cv.findContours(canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

#Tìm trung điểm các cạnh
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) / 2, (ptA[1] + ptB[1]) / 2)

#Tính toán kích thước thật của vật thể  
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
    cv.putText(img, "{:.1f} mm".format(Hr), (int(Hx - 15), int(Hy)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
    cv.putText(img, "{:.1f} mm".format(Wr), (int(Ex), int(Ey-10)), cv.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
print(Wr,Hr) 
cv.imshow('canny1',canny1)
cv.imshow('canny',canny)
cv.imshow('result',img)
cv.waitKey(0)
cv.destroyAllWindows