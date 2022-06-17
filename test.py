import cv2 as cv



img = cv.imread('image_19.png',cv.IMREAD_COLOR)
img = cv.resize(img, dsize=(600, 600))

cv.imshow('result',img)
cv.waitKey(0)
cv.destroyAllWindows