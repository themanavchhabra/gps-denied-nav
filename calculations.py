import numpy as np

class Calculations():
    def __init__(self):
        print("hello")

    def rotationMatrix3D(r,p,y):
        rmatrix = np.array([[np.cos(p)*np.cos(r),(np.sin(y)*np.sin(p)*np.cos(r))-(np.cos(y)*np.sin(r)),(np.cos(y)*np.sin(p)*np.cos(r))+(np.sin(y)*np.sin(r))],
                            [np.cos(p)*np.sin(r), (np.sin(y)*np.sin(p)*np.sin(r))-(np.cos(y)*np.cos(r)), (np.cos(y)*np.sin(p)*np.sin(r))+(np.sin(y)*np.cos(r))],
                            [-np.sin(p), np.sin(y)*np.cos(p), np.cos(y)*np.cos(p)]]) #3D rotation matrix
        
        return rmatrix
