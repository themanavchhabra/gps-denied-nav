import numpy as np
import math
from geopy.distance import geodesic


class Calculations():
    def __init__(self):
        print("hello")

    def rotationMatrix(self,r,p,y):

        rmatrix = np.array([[np.cos(p)*np.cos(r),(np.sin(y)*np.sin(p)*np.cos(r))-(np.cos(y)*np.sin(r)),(np.cos(y)*np.sin(p)*np.cos(r))+(np.sin(y)*np.sin(r))],
                            [np.cos(p)*np.sin(r), (np.sin(y)*np.sin(p)*np.sin(r))-(np.cos(y)*np.cos(r)), (np.cos(y)*np.sin(p)*np.sin(r))+(np.sin(y)*np.cos(r))],
                            [-np.sin(p), np.sin(y)*np.cos(p), np.cos(y)*np.cos(p)]]) #3D rotation matrix

        rmatrix2D = np.array([[np.cos(y), -np.sin(y)],[np.sin(y), np.cos(y)]])

        return rmatrix2D

    def get_actual_distance(self,x,y,z,loc_starting, loc_current):
        print("loc_current is " + str(loc_current))
        print("loc_starting is " + str(loc_starting))
        off_x = loc_current.lon - loc_starting.lon
        off_y = loc_current.lat - loc_starting.lat
        bearing = math.atan2(-off_y, off_x)

        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        distance = geodesic((loc_current.lat, loc_current.lon), (loc_starting.lat, loc_starting.lon)).meters
        print(distance)
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")

        print("bearing is " + str(bearing))

        print((x,y,z))

        x = distance*np.sin(bearing)
        y = distance*np.cos(bearing)

        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        print((x,y,z))
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")


        return((x,y,z))