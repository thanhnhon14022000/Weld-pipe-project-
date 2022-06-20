import cv2 as cv

cam = cv.VideoCapture(0)




while True:
    ret, frame = cam.read()
    cv.imshow("test", frame)
    if not ret:
        break
    k = cv.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    

cam.release()

cv.destroyAllWindows()