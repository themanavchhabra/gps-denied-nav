import logging
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import filters
import calculations
import pixhawk

# FOV of camera at resolution (1280*720)
hfov = 73.387
vhov = 45.462

# vid = cv2.VideoCapture(0)
frame = cv2.imread('sample.jpg')

# Shi Tomasi feature detection algorithm parameters
feature_params = dict(maxCorners=50, # number of features
                      qualityLevel=0.001, # quality of features
                      minDistance=10, # minimum distance between features in pixels
                      blockSize=7)

# Lucas Kanade Feature Tracking Algorithm parameters
lk_params = dict(winSize=(15, 15), # size of image around the feature to be considered for tracking
                 maxLevel=4,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

log_x = open("x.txt", "w")              
log_xfil = open("x_filtered.txt", "w")  
log_xact = open ("x_actual.txt", "w")   
# optical_flow_logs = open("optical_flow_logs.txt" , "w") 

calc = calculations.Calculations()
pix = pixhawk.Pixhawk("127.0.0.1:14550")


class Visual_Odometry():

    def __init__(self, source, initial_height):
        print("init done")
        self.source = cv2.VideoCapture(source)
        self.source.set(3, 1280) # setting the camera frame width to 1280
        self.source.set(4, 720) # setting the camera frame height to 720
        self.frame_width = int(self.source.get(3)) # frame width of the source
        self.frame_height = int(self.source.get(4)) # frame height of the source
        self.initial_height = initial_height
        self.old_gray = None # previous frame
        self.p0 = None # features of the previous frame
        self.delta_time = None # time interval for each call
        self.last_height = None # height during the last call
        self.delta_time = None # angle of yaw
        self.rtheta = None
        self.disx = 0
        self.disy = 0
        self.filter = filters.Filters() # initializing the filters class object for low pass filter
    

    def displacement_pixel(self, old_points, new_points, h):

            # print("displacement_pixel function invoked , new points is %s" %str(h)) #MC 

            """
            The distance (in pixels) between the features in a frame varies with height (distance reduces with increase in
            height and vice versa). Therefore, a projection of the old features is taken at the new height before taking
            the difference with the new features and averaging it.
            :param old_points: features of the previous frame
            :param new_points: features of the current frame
            :param h: current height of the UAV
            Returns: a tuple of the average displacement (in pixels) between 2 set of features
            """
            l = len(old_points) #number of features
            if l == 0: # if the number of features is 0
                return (0, 0)
            if self.last_height: # if the last height is displacement_pixel function invokednot None
                v1 = (old_points - np.array([self.frame_width, self.frame_height]) / 2) # shifting the origin of the old features from the top left corner to the cnetre of the frame
                v2 = v1
                if h != 0: # if the new height is not 0
                    v2 = (self.last_height / h * v1 + np.array([self.frame_width, self.frame_height]) / 2) # taking the projection of the old features at current height of the UAV
                avg_x = sum((new_points[0:, 0:, 0:1] - v2[0:, 0:, 0:1]).ravel()) / l # averaging the difference along x axis
                avg_y = sum((new_points[0:, 0:, 1:2] - v2[0:, 0:, 1:2]).ravel()) / l # averaging the difference along y axis
                return (avg_x, avg_y)
            # if current height is 0 or last height is None
            avg_x = sum((new_points[0:, 0:, 0:1] - old_points[0:, 0:, 0:1]).ravel()) / l # averaging the difference along x axis
            avg_y = sum((new_points[0:, 0:, 1:2] - old_points[0:, 0:, 1:2]).ravel()) / l # averaging the difference along y axis
            return (avg_x, avg_y)

    def frame_process(self, h, log_x, log_xfil, log_xact):
        """
        Takes frame from the video source. Extracts and tracks features on the frame.
        :param h: current height of the UAV
        :param bearing: current bearing of the UAV
        :param optical_flow_logs: file object to write estimated (lat, long) and (bearing, altitude)
        Returns: estimated lat, estimated long, instantaneous dx, instantaneous dy, number of features to be tracked in the next call
        """

        _, frame = self.source.read() # reading frame from the source
 #       out.write(frame)

        self.rtheta = pix.get_attitude() #gets the attitude of the drone 

        # capturing first features
        if self.old_gray is None: # during the first call of the function as we don't have the old frame and old features
            self.old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # setting the frame to be old frame
            self.p0 = cv2.goodFeaturesToTrack(self.old_gray[40:self.frame_height-40, 40:self.frame_width-40], mask=None, **feature_params) + np.array(
                [40, 40], dtype=np.float32) # finding features on the frame using Shi Tomasi algorithm, leaving a pixel width of 40 pixels on the border of the frame
            return 0, 0, len(self.p0) #returning the home location and (0, 0) as (dx, dy) as no fetures were tracked in the first call
        
        if self.rtheta is not None and self.p0 is not None:
            angle = self.rtheta
            # rmatrix = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
            rmatrix = calc.rotationMatrix3D(angle[0],angle[1],angle[2]) #gets the rotation matrix from the attitude angles
            self.p0 = np.matmul(self.p0, rmatrix)


        # The following part executes from the 2nd call of the function as we now have the old frame and old features
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), self.p0, None,
                                               **lk_params) # tracking the old features
        ndel = [] # list to delete the erroneous features
        n_points = len(p1) # number of features tracked
        status = st.ravel() # status of the features (0 if it is not present in the current frame else 1)
        #print(p1)
        for i in range(len(p1)): # iterating over the numpy array of features
            xa, ya = p1[i].ravel() # reducing the dimensions to 1 and (xa, ya) is the position of the feature
            if not 20 < xa < self.frame_width-20 or not 20 < ya < self.frame_height-20 or status[i] == 0: # excluding features which lie inside or outside a pixel width of 20 pixels from the border of the frame
                n_points -= 1
                ndel.append(i) # adding the index of the feature to be deleted if the list ndel
        p1 = np.delete(p1, ndel, 0) # deleting the list of erroneous features from the current numpy array of features
        self.p0 = np.delete(self.p0, ndel, 0) # deleting the list of erroneous features from the previous numpy of features
        st = np.delete(st, ndel) # deleting the list of erroneous features from the current numpy array of status

        (x, y) = self.displacement_pixel(self.p0, p1, h) # calculating displacement in pixels
        x = -x * 2 * h * math.tan(hfov * math.pi / 360) / self.frame_width   # calculating displacement in x in mts (here the negative sign is due to the dfference in frame of reference of the UAV and the camera... THINK CAREFULLY)
        y = y * 2 * h * math.tan(vhov * math.pi / 360) / self.frame_height    # calculating displacement in y in mts
        # print("from frame process , upar wala x is " + str(x) + " and upar wala y is " + str(y))

        self.disx += x # updating the current x position
        self.disy += y # updating the current y position
        # optical_flow_log =str(h) + '\n' # creating log to be written
        # optical_flow_logs.write(optical_flow_log) # writing the estimated location, current bearing and current altitude to the file

        if (n_points < 31): # estimating more features in the frame if the number of features fall below 31
            pnew = cv2.goodFeaturesToTrack(self.old_gray[40:self.frame_height-40, 40:self.frame_width-40], mask=None, **feature_params) + np.array(
                [40, 40],
                dtype=np.float32)
            p1 = np.concatenate((p1, pnew), axis=0) # concatenating the new features to the current numpy array of features

        self.old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # updating the old frame to the current frame for the next call of the function
        self.p0 = p1 # updating the old features to current features for the next call of the function

        self.disx += x # updating the current x position
        self.disy += y # updating the current y position

        xlog = str(self.disx) + " " + str(self.disy) + "\n" #log to be written
        log_x.write(xlog) #logginf the distance x and y from home 
        # print("from frame process function x is " + str(self.disx) + " and y is " + str(self.disy))

        timeconstant = ((0.5 - 0.1) / 50 * h)

        filx = self.filter.lowpass(self.disx, self.delta_time, 0.1 + timeconstant) #filtering current x postion 
        fily = self.filter.lowpass(self.disy, self.delta_time, 0.1 + timeconstant) #filtering current y positon

        filxlog = str(filx) + " " + str(fily) + "\n" #log to be written , filtered position
        log_xfil.write(filxlog) #logginf the distance x and y from home , filtered

        # kalx = self.filter.kalman(self.disx)
        # kaly = self.filter.kalman(self.disy)

        # actxlog = str("""actual x """) + " " + str("""actual y """) + str(h) + "\n" #log to be written , actual  position
        # log_xact.write(actxlog) #logginf the distance x and y from home , actual from pixhawk

        return self.disx, self.disy, n_points

    def __call__(self,delta_time):
        """
        The call is callable.
        :param delta_time: time difference between the last call and current call.
        """
        self.delta_time = delta_time # setting the class attribute delta_time
        if not delta_time: # is delta_time is 0 or None (NEVER HAPPENED)
            self.delta_time = 0.07
        # self.Time += self.delta_time # updating time of flight
      #  print("TIMEEEEEEEEEEEEEE", self.Time)
        # try:

        h = self.initial_height

        dis_x, dis_y, n_points = self.frame_process(h, log_x, log_xfil, log_xact) # proesssing the video frame ( _test function can be used during simulation.)





