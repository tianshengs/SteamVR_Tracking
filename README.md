# Extracting data from SteamVR using HTC VIVE tracker

The goal of this project is to extract useful pose data using the HTC VIVE tracker to pass to the UR5 robot arm through Rosvita, so that the robot arm could imitate the motion of the tracker. The program is designed for windows and only works on windows due to the compatibility of SteamVR.

The program uses triad_openvr.py script from [triad_openvr](https://github.com/TriadSemi/triad_openvr).

## Getting Started

These instructions will illustrate how to set up the environment required for the program to run.

### Setting up the Base Station

Mount the base station in your room (recommend using a tripod). Use one base station should be enough. Here are some things that you need to pay attention to when you mount the base station:

- Mount the base station high up in the room (above your height). The tracker cannot be detected if the base station is too low or too close to the tracker.

- Make sure that the base station is plugged in and mounted stably, any movement of the base station will disconnect it from the tracker.

- Change the mode of the base station to “b” by using the button on the back.

### Prerequisites

This section is adapted from [SteamVR Tracking without an HMD](http://help.triadsemi.com/en/articles/836917-steamvr-tracking-without-an-hmd). All the detailed instructions could be found on the website.

1. In order for the program to run, you must have the latest version of SteamVR, with opted in for the beta, then change some settings in order to track without an HMD:

	1. Download [Steam](https://store.steampowered.com/about/) to your Windows PC. Create an account and log into Steam.  
	1. Locate SteamVR in the Library tab, and download it.
	1. Right click on SteamVR, select Properties-> Beta, change the first option to "beta - SteamVR Beta Update" in order to opt in for the beta.
	1. After Steam finishes downloading SteamVR beta, right click on SteamVR, select Properties-> Local Files-> Browse Local Files to browse local files.
	1. Locate this file and open it with a text editor:
			steamapps/common/SteamVR/drivers/null/resources/settings/default.settings
	1. Change “enable” to true

	1. Save the file and close it. Then locate this file:
			steamapps/common/SteamVR/resources/settings/default.settings

	1. Set the following keys under “steamvr” to the followings:
			“requireHmd”: false;
			“forcedDriver”: “null”;
			“activateMultipleDrivers”: true;
	1. Save this default.vrsettings file and close
	1. Once successfully set up SteamVR, you can now hit “Play” to start SteamVR. If SteamVR is running, close and restart it. you will see that it is now possible to connect a tracker or controller without the HMD.

2. In order for the program to run, you should have Python 3.6 running on your computer.

3. Once Python 3.6 is installed, use pip to install [pyopenvr](https://github.com/cmbruns/pyopenvr) and [pyquaternion](http://kieranwynn.github.io/pyquaternion/) with the following commands:

	```
	pip install openvr
	pip install pyquaternion
	pip install matplotlib
	```

4. Now you have installed all the required prerequisites for this program. To have the program running on local environments, simply clone this GitHub repository to a local folder, and you are ready to run the program.

## Running the program

Before running the program, you first need to run SteamVR, then connect the VIVE tracker to your computer(either using the USB cable, or wirelessly using the dongle and dongle cradle). Hold the button on the tracker for one second to turn on the tracker. Make sure that there is nothing between the base station and the tracker, so that the IR light sent by the base station could be detected by the tracker. When everything is connected, you will see that the base station symbol and the tracker symbol of steamVR turn green(without flashing). The light on the tracker should also turn green when it is tracking. Note that the “Not Ready” text is normal.

### Examine the real-time pose information of tracker using tracker_test.py

Once both the tracker and the base station are connected, you could run the following command to check the real-time pose data of the tracker:

```
python3 tracker_test.py
```

As the script executes, you will see numbers updating at 250Hz. The first three numbers are the Cartesian coordinates of the tracker in the order of X, Y, Z. The next four numbers are the quaternions of the tracker in the order of w, x, y, z.

The coordinates of the VR world are set up like this: when facing towards the base station, in your front is the +z direction, above you is the +y direction, and to your left is the +x direction.

### Record a session of pose movement and send it to robot arm

#### Recording data on the windows PC using record_track.py

In order to record a session of pose movement, run the following command after both base station and tracker are connected:

```
python3 record_track.py [duration = 5] [interval = 0.05]
```

The program takes two optional arguments, the first argument is the duration of motion you want to record in seconds. The default value for duration is 5 seconds. The second argument is the time interval between every pose information in seconds. The shorter the interval, the more accurate the record data are. The default value for interval is 0.05 second.

Once the program is executed, it will prompt you to hit enter. The recording starts as soon as you hit the enter key, and will finish when the time of duration elapses. Afterwards, the program will ask the name of file you would like to save(default is "test"). Then in the same directory, you should see a generated .obj file that contains all the recorded poses. A .png file will also be generated, which contains three graphs that shows the change of Catesian Coordinate, change of Quaternion, and velocity, respectively.

Here is a sample .png file that you may get:
![test](https://user-images.githubusercontent.com/25497706/61661136-6b332b00-ac99-11e9-82f6-07827b5e8a3f.png)


#### Execute the recorded motion on robot arm

Once having the .obj file, you should transfer the .obj file to the ubuntu machine which runs Rosvita(either through email or flash drive). Then, in the Rosvita server, navigate to the folder where the script motion_track.py is located, and upload the .obj file to the same folder. In the command line of Rosvita, execute the following command(it is recommended first running the script in simulation mode):

```
python3 motion_track.py
```

Then, you should see the (simulated) robot arm carry out the recorded movements from motion capture data.

## Notes
- Check triad_openvr.py for all the possible data that you may get: get_pose_euler, get_pose_quaternion, get_velocity, get_angular_velocity, and get_pose_matrix.

- To save the pose data and use it on a robot arm, we calculate the delta value (difference) between the beginning pose and the subsequent ones.

- For the pose data to fully work on a robot arm, you also have to convert the coordinates from the ones in the VR world to the ones the robot arm is using.

- Try to use quaternion for more stable orientation data. Euler angles, although easier to comprehend, can be very unstable and lead to problems such as Gimbal Lock.

## Author

* Tiansheng Sun

* Guanghan Pan

## Acknowledgments

* Thanks to Professor Daniel Scharstein from Middlebury College for overseeing this project.

* The program triad_openvr.py and tracker_test.py are downloaded and adapted from [triad_openvr](https://github.com/TriadSemi/triad_openvr).
