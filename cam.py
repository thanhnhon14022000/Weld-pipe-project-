import cv2 as cv
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



cam = cv.VideoCapture(1)

while True:
    ret, frame = cam.read()
    
    if not ret:
        break
    k = cv.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    frame = cv.resize(frame, dsize = (sizeH,SizeW))
    cv.line(frame,(center,sizeH),(center,0),(0,255,0),1)

    # cv.line(frame,(0,100),(600,100),(255,255,0),2)
    cv.rectangle(frame,(rightframe,sizeH) , (leftframe, 0), (0,0,255),1)
    #NGANG 
    cv.line(frame,(0,300),(600,300),(0,255,0),1)
    cv.imshow("test", frame)
cam.release()

cv.destroyAllWindows()