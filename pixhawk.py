import dronekit as dk 
from dronekit import connect
from geopy.distance import geodesic
import numpy as np
import cv2

# connection_string = "127.0.0.1:14550"


class Pixhawk():

    def __init__(self, connection_string):
        try:
            self.vehicle = connect(connection_string)
            print("connected")
        except:
            print("not connected")

    def get_attitude(self):
        r,p,y = self.vehicle.attitude.roll, self.vehicle.attitude.pitch, self.vehicle.attitude.yaw #gets atttide of drone 
        print("got attitude")
        print((r,p,y))

        return((r,p,y))



    # print(vehicle.attitude.yaw)
    # print(vehicle.location.local_frame)

    def actual_distance(self):
        x= self.vehicle.location.local_frame.north * np.sin(self.vehicle.attitude.yaw)
        y = self.vehicle.location.local_frame.east * np.cos(self.vehicle.attitude.yaw)
        z = -self.vehicle.location.local_frame.down

        print(x,y,z)