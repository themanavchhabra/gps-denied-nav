import dronekit as dk 
from dronekit import connect
from geopy.distance import geodesic
import numpy as np
import cv2

try:
    vehicle = connect("127.0.0.1:14550")
    print("connected")
except:
    print("not connected")

print(vehicle.attitude.yaw)
print(vehicle.location.local_frame)

x= vehicle.location.local_frame.north * np.sin(vehicle.attitude.yaw)
y = vehicle.location.local_frame.east * np.cos(vehicle.attitude.yaw)
z = -vehicle.location.local_frame.down
print(x,y,z)

# Abuja =(9.072264 , 0)
# Dakar =(14.716677 , 0)
# #Finally, print the distance between the two sites in kilometers.
# print("The distance between Abuja and Dakar is: ", geodesic(Abuja,Dakar).km)



# class drone():
    