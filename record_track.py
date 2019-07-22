#!/usr/bin/env python3

import triad_openvr
import time
import sys
import numpy as np
import pickle
import math
import matplotlib.pyplot as plt
from pyquaternion import Quaternion
import socket

HOST = '192.168.1.102'  # The server's hostname or IP address
PORT = 65431        # The port used by the server

v = triad_openvr.triad_openvr()
debug = 0
real_time = 1
record_time = 0.4

#Function that saces the figure of euler, quaternion and velocity
def save_figure(data,name):
    index = []
    x = []
    y = []
    z = []
    r_w = []
    r_x = []
    r_y = []
    r_z = []
    v_x = []
    v_y = []
    v_z = []
    
    for i in range(len(data)):
        coordinate = data[i][:3]
        quat_element = data[i][3:7]
        velocity = data[i][7:]
        index.append(i)
        x.append(coordinate[0])
        y.append(coordinate[1])
        z.append(coordinate[2])
        r_w.append(quat_element[0])
        r_x.append(quat_element[1])
        r_y.append(quat_element[2])
        r_z.append(quat_element[3])
        v_x.append(velocity[0])
        v_y.append(velocity[1])
        v_z.append(velocity[2])              

    plt.subplots(1,3,figsize=(18,5))
    plt.subplot(1,3,1)
    plt.plot(index,x, label="x")
    plt.plot(index,y, label="y")
    plt.plot(index,z, label="z")
    plt.title("Change of Cartesian Coordinate")
    plt.xlabel("index number")
    plt.ylabel("coordinate diff")
    plt.legend()

    plt.subplot(1,3,2)
    plt.plot(index,r_w, label="r_w")
    plt.plot(index,r_x, label="r_x")
    plt.plot(index,r_y, label="r_y")
    plt.plot(index,r_z, label="r_z")
    plt.title("Change of Quaternion")
    plt.xlabel("index number")
    plt.ylabel("quaternion diff")
    plt.legend()

    plt.subplot(1,3,3)
    plt.plot(index,v_x, label="v_x")
    plt.plot(index,v_y, label="v_y")
    plt.plot(index,v_z, label="v_z")
    plt.title("Velocity")
    plt.xlabel("index number")
    plt.ylabel("velocity")
    plt.legend()
    plt.savefig("%s.png"%name)

if __name__ == "__main__":
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
        start_quaternion = Quaternion(start_point[3:])
        record = []
        if real_time:
            path = []
            last_record = time.time()

        # start recording
        while(time.time()-start_time < duration):
            start = time.time()
            current = np.array(v.devices["tracker_1"].get_pose_quaternion())
            velocity = v.devices["tracker_1"].get_velocity()
            if current.all():
                current_location = current[0:3]
                location_diff = current_location - start_location
                current_quaternion = Quaternion(current[3:])
                quaternion_diff = current_quaternion * start_quaternion.inverse
                pose = [round(x,6) for x in location_diff] + [round(x,6) for x in quaternion_diff.elements]
                record.append(pose + velocity[:])
                print(pose+velocity[:])


                if(real_time and time.time()- last_record > record_time):
                    last_record = time.time()
                    path.append(pose)

                    if(len(path) == 10):
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT))
                            s.sendall(str(path).encode('UTF-8'))
                            path = []

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
            save_figure(record,name)
        else:
            print("data collection failed")


