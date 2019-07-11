Setting up the StreamVR system without an HMD to capture pose data using HTC VIVE
Written by Tiansheng Sun

This documentation illustrates how to set up and use the StreamVR system to capture pose (position and orientation) data using the HTC VIVE tracker without an HMD on a Windows computer. The captured data can then be used for a robot arm so that the robot arm can move just like how the tracker moves. 

1:  Mount the base station in your room. Using one base station should be enough. Here are some things that you need to consider when you mount the base station:

	a. Mount the base station high up in the room (above your height). The tracker cannot be detected if the base station is too low or close to the tracker.

	b. Make sure that the base station is plugged in and mounted stably. 

	c. Change the mode of the base station to “b”.


2:  Download Stream to your Windows PC. After you finish downloading Stream, create an account and log in to Stream. 


3:  Go to “Library”, select “StreamVR” and download it.  


4: Get access to the SteamVR files, right click on SteamVR, select Properties-> Local Files-> Browse Local Files to browse local files. 


5:  Since we want to track without an HMD, we have to change the setting of two SteamVR files:

	a. Locate this file: 
	    steamapps/common/SteamVR/drivers/null/resources/settings/default.settings

	b. Change “enable” to true 

	c. Save the file and close it. Then locate this file: 
	    steamapps/common/SteamVR/resources/settings/default.settings

	d. set the following keys under “steamvr” to the followings:
	    key “requireHmd”: false;
	    key “forcedDriver”: “null”;	
	    key “activateMultipleDrivers”: true;

e. Save the file and close it.


6:  Once we successfully set up SteamVR, we can now hit “Play” to start SteamVR. If SteamVR is running, close and restart it. We should not worry too much about Room Setup.


7：  Make sure that Python 3.6 is installed. 


8：  Once Python 3.6 is installed, use the command pip install openvr to install pyopenvr.


9：  Download triad_openvr from github page: https://github.com/TriadSemi/triad_openvr. This function contains tracker_test.py that can capture position and orientation data of the tracker.


10：  Connect the tracker to your computer. Hit the button on the tracker to turn on the tracker. When everything is connected, you will see that the base station symbol and the tracker symbol of steamVR turn green (without flashing). The light on the tracker should also turn green when it is tracking. Note that the “Not Ready” text is normal. 


11：  Once both the tracker and the base station are connected, run tracker_test.py to see the numbers updating at 250HZ. Note that the numbers shown are X, Y, Z coordinates and yaw, pitch, and roll (euler angles). If you want quaternion angles, change get_pose_euler in tracker_test.py to get_pose_quaternion. 


Notes on getting pose data and running them on a robot arm:
	
	a. Check triad_openvr.py for all the possible data that you may get. Besides get_pose_euler and get_pose_quaternion, you can also get velocity (get_velocity), angular velocity (get_angular_velocity), and pose matrix (get_pose_matrix). 

	b. To save the pose data and use it on a robot arm, consider calculating the delta value (difference) between the beginning pose and the subsequent ones.  I wrote the file Record_trak.py that calculates the difference between the beginning pose and the subsequent ones and store them into an .obj file.

	c. For the pose data to fully work on a robot arm, you also have to convert the coordinates from the ones in the VR world to the ones the robot arm is using. The coordinates of the VR world are set up like this:
	   Facing towards the base station, in your front is the +z direction, above you is the +y direction, and to your left is the +x direction.

	d. Try to use quaternion for more stable orientation data. Euler angles, although easier to comprehend, can be very unstable and lead to problems such as Gimbal Lock. 

Useful python module:

	pyquaternion, a python module for representing and using quaternions: http://kieranwynn.github.io/pyquaternion/
	
References:

	Reid Wender: http://help.triadsemi.com/en/articles/836917-steamvr-tracking-without-an-hmd
