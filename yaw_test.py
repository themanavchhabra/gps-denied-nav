import cv2
import numpy as np

src = "yawtestimg.jpg"

img = cv2.imread(src)

feature_params = dict(maxCorners=50, # number of features
                      qualityLevel=0.001, # quality of features
                      minDistance=10, # minimum distance between features in pixels
                      blockSize=7)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

features = cv2.goodFeaturesToTrack(img, **feature_params)

print(features)

angle = np.pi

rmatrix = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])

print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

print(np.matmul(features, rmatrix))

cv2.imshow('image',img)
cv2.waitKey(0)