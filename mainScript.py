import getx
import time

height = 75

getxCall = getx.Visual_Odometry(-1,height)
delta_time=0.1

while True:
    starttime = time.time()
    getxCall(delta_time)
    delta_time = time.time() - starttime