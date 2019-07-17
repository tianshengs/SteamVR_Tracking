import triad_openvr
import time
import sys
import numpy as np
import pickle
import math
from pyquaternion import Quaternion

v = triad_openvr.triad_openvr()
debug = 0

if len(sys.argv) == 1:
    duration = 5
    interval = 1/20
elif len(sys.argv) == 2:
    duration = float(sys.argv[1])
    interval = 1/20
elif len(sys.argv) == 3:
    duration = float(sys.argv[1])
    interval = float(sys.argv[2])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    input("Press Enter to start (duration = %s seconds, interval = %s seconds)"%(duration, interval))
    start_time = time.time()
    start_point = v.devices["tracker_1"].get_pose_quaternion()
    start_location = np.array(start_point[0:3])
    start_quaternion = Quaternion(start_point[3], start_point[4], start_point[5], start_point[6])
    record = []
    while(time.time()-start_time < duration):
        start = time.time()
        current = np.array(v.devices["tracker_1"].get_pose_quaternion())
        velocity = v.devices["tracker_1"].get_velocity()
        if current.all():
            current_location = current[0:3]
            location_diff = current_location - start_location
            current_quaternion = Quaternion(current[3], current[4], current[5], current[6])
            quaternion_diff = current_quaternion * start_quaternion.inverse
            record.append([location_diff, quaternion_diff, velocity])
        sleep_time = interval - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
    if debug:
        print(record)
    if record:
        print("data collection success!")
        name = input("Enter the name of file:")
        if not name:
            name = "test"
        file_path = open('%s.obj'%name, 'wb')
        print("saved as %s.obj"%name)
        pickle.dump(record, file_path)
    else:
        print("data collection failed")
   
