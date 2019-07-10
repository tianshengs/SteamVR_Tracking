"""
Tiansheng Sun 
July 2019 
reecord_track.py
This file is used to track with certain intervals in a giver duration and save 
pose (position and orientation) data of HTC VIVE tracker in SteamVR system.
"""

import triad_openvr
import time
import sys
import numpy as np
import pickle
import math
from pyquaternion import Quaternion

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

def euler_to_quaternion(yaw, pitch, roll):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) + np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qw, qx, qy, qz]

def quaternion_to_euler(w, x, y, z):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z

#set the default interval 
if len(sys.argv) == 1:
    interval = 1/20
#or set up the user-given custormized interval
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

if interval:

    #when ready, hit enter to capture poses
    input("hit enter")
    
    start_time = time.time()
    
    #get the starting pose
    start_point = v.devices["tracker_1"].get_pose_quaternion()
    start_location = np.array(start_point[0:3])
    start_quaternion = Quaternion(start_point[3], start_point[4], start_point[5], start_point[6])
    record = []
    #set the total duration 
    duration = 5
    
    while(True):
        start = time.time()
        
        #get the current pose
        current = np.array(v.devices["tracker_1"].get_pose_quaternion())
       
        if current.all():
            current_location = current[0:3]
            current_location = current_location - start_location
            current_quaternion = Quaternion(current[3], current[4], current[5], current[6])
            current_quaternion = current_quaternion * start_quaternion.inverse
            record.append([current_location, current_quaternion])
            
        if (time.time() - start_time > duration):
            break
            
        sleep_time = interval - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
            
    #Save all the pose data into "test.obj" file        
    file_path = open('test.obj', 'wb')
    pickle.dump(record, file_path)
