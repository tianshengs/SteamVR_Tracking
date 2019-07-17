import triad_openvr as vr
import matplotlib.pyplot as plt
from pyquaternion import Quaternion
import pickle
import sys

if len(sys.argv) == 2:
    try:
        file_path = open("%s.obj"%(sys.argv[1]), 'rb') 
    except:
        print("file does not exist")
    else:
        data = pickle.load(file_path)
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
            coordinate = data[i][0]
            quat_element = data[i][1].elements
            velocity = data[i][2]
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

        plt.show()
else:
    print("usage: python plot_graph.py [data name]")
        
