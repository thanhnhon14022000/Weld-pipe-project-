import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('Test/corona.jpg',cv.IMREAD_COLOR)
img = cv.resize(img, dsize=(600, 600))
cv.imshow('corona', img)
cv.waitKey(0)
cv.destroyAllWindows()