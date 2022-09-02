import numpy as np
import math


class Calculations():
    def __init__(self):
        print("hello")

    def rotationMatrix3D(self,r,p,y):
        rmatrix = np.array([[np.cos(p)*np.cos(r),(np.sin(y)*np.sin(p)*np.cos(r))-(np.cos(y)*np.sin(r)),(np.cos(y)*np.sin(p)*np.cos(r))+(np.sin(y)*np.sin(r))],
                            [np.cos(p)*np.sin(r), (np.sin(y)*np.sin(p)*np.sin(r))-(np.cos(y)*np.cos(r)), (np.cos(y)*np.sin(p)*np.sin(r))+(np.sin(y)*np.cos(r))],
                            [-np.sin(p), np.sin(y)*np.cos(p), np.cos(y)*np.cos(p)]]) #3D rotation matrix

        return rmatrix

    def get_actual_distance(x,y,loc_starting, loc_current):
        off_x = loc_current.lon - loc_starting.lon
        off_y = loc_current.lat - loc_starting.lat
        bearing = math.atan2(-off_y, off_x)

        x = off_x*np.sin(bearing)
        y = off_y*np.cos(bearing)

        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print((x,y))
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")


        return((x,y))