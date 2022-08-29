from filterpy.kalman import KalmanFilter
import numpy as np
from filterpy.common import Q_discrete_white_noise


class Filters():


    def __init__(self):
        self.last_output = None
        self.output_queue = list()
        self.flag = 0

        self.f = KalmanFilter(dim_x=2, dim_z=1)
        self.f.x = np.array([2])
        self.f.F = np.array([1.,1.])
        self.f.H = np.array([[1.,0.]])
        self.f.P *= 1000.
        self.f.R = 5
        self.f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)


    def lowpass(self,input, dt ,timeconstant):
        alpha = dt / ( timeconstant + dt)
        # print (alpha)
        if self.flag == 0:
            output = input
            self.flag = 1
        else :
            output = (alpha * input) + ((1-alpha) * self.last_output)
            

        self.last_output = output
        return (output)

    def kalman(self, input):
        output = input
        self.f.predict()
        self.f.update(output)
        
        return(output)
