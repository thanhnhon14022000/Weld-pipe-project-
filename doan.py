from re import L
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from imutils import perspective
from scipy.spatial import distance as dist

# Dimension constant
alpha = 4
beta = 0
sizeH = 600
SizeW = 600
center = int(sizeH / 2)
dimensionDrop = 20
leftframe = 290
rightframe = 310
centerFrame = int((rightframe-leftframe/2))

# function returns current size of pipe
def dimensition(size): 
    global scale
    
    #coefficient that returns the true size of the pipe
    scale = 3
    size = int(size / scale)
    if size <= 25:
        size = 21
    if size > 25 and size < 30:
        size = 27
    if size >=30 and size < 38:
        size = 32
    if size >= 38 and size < 45:
        size = 42
    if size >=45 and size < 54:
        size = 48
    if size >=54:
        size = 60
    return size

#The function returns the midpoint of the line
def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) / 2, (ptA[1] + ptB[1]) / 2)

# function that returns the size of the pipe
def processDimension(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    canny = cv.Canny(img_gray,20,100)
    kenel = cv.getStructuringElement(cv.MORPH_RECT,(9,9))
    out_1 = cv.morphologyEx(canny,cv.MORPH_CLOSE,kenel,iterations=1)

    contour, hierachy = cv.findContours(out_1,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cv.imshow('123',canny)
    for c in contour:
        global a
        if cv.contourArea(c) < 3000:
            continue
        box = cv.minAreaRect(c)
        box = cv.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)        
        # cv.drawContours(img,[box.astype("int")], -1, (0, 255, 0), 2)
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
        if a is None:
            a=25
        print('Kich thuoc cua ong sau khi scale',a)
        # cv.putText(img, "{:.1f} mm".format(Hr), (int(Hx - 15), int(Hy)), cv.FONT_HERSHEY_SIMPLEX, 1,
        #                 (0, 0, 255), 2)
        # cv.putText(img, "{:.1f} mm".format(Wr), (int(Ex), int(Ey-10)), cv.FONT_HERSHEY_SIMPLEX, 1,
        #                 (0, 0, 255), 2)
    return a
def detectWeld(img):
    global weld

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray_ct = cv.addWeighted(img_gray, alpha, np.zeros(img_gray.shape, img_gray.dtype), 0, beta)

    blur_img = cv.blur(img_gray_ct, (7,7))
    binary_img = cv.adaptiveThreshold(blur_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 2)
    binary_img = cv.erode(binary_img, None, iterations=2)
    skeleton_img = cv.ximgproc.thinning(binary_img, 0)

    lines = cv.HoughLinesP(skeleton_img, 1, np.pi/180, 20, minLineLength=30, maxLineGap=10)
    if lines is None:
        print('Khong tim thay lines')
    for line in lines:
        x1,y1,x2,y2 = line[0]
        if(abs(x1-x2)) < 5:
            weld = line[0]
            print(line)
            cv.line(img,(x1,y1),(x2,y2),(255,0,0),1)

    if weld[0] > leftframe and weld[0] < rightframe:
            print('Mối hàn đã vào tâm') 
    cv.imshow("456",skeleton_img )

cap = cv.VideoCapture(1)

if not cap.isOpened(): # kiem tra xem video có hoat dong khong
    print('can not open video clip/camera')
    exit()

while True: # su lý video can while true
    # read frame by frame
    ret, frame = cap.read() #frame luu gia tri bo nho
    if not ret:
        print(' can not read video frame. Video ended?')
        break
    # frame = cv.rotate(frame, cv.cv2.ROTATE_90_CLOCKWISE)
    frame = cv.resize(frame, dsize = (sizeH,SizeW))
    b = processDimension(frame)
    frame_drop = frame[270:330,:]
    # detectWeld(frame_drop)
    #Camera center line and center frame
    cv.line(frame,(center,sizeH),(center,0),(0,255,0),1)
    cv.rectangle(frame,(rightframe,sizeH) , (leftframe, 0), (0,0,255),1)
    

    

    cv.imshow('video', frame)
    # close clip
    cv.imshow('frame_drop', frame_drop)
    
    if cv.waitKey(2) == ord('q'):
        break
cap.release() # xoa vung bo nho
cv.destroyAllWindows()