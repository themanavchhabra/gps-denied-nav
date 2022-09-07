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

    def get_curr_height(self):
        return self.vehicle.location.local_frame.down

    def get_home(self):
        while not self.vehicle.home_location:
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            if not self.vehicle.home_location:
                print(" Waiting for home location ...")
            
            print("home at " + str(self.vehicle.home_location))
            return(self.vehicle.home_location)

    # print(vehicle.attitude.yaw)
    # print(vehicle.location.local_frame)

    def loc_current_relative(self):
        x = self.vehicle.location.local_frame.north
        y = self.vehicle.location.local_frame.east
        z = -self.vehicle.location.local_frame.down

        return(x,y,z)

    def loc_current(self):
        print("into loc current function")
        print("current location is " + str(self.vehicle.location))
        return self.vehicle.location.global_frame