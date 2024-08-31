# Rover - docking
Repository containing code space to dock rover into the drone container.

![color segmentation](https://github.com/Sanidhya-30/rover-docking/blob/main/colospace_segmentation.jpeg)

## Key Feature:-
* HSV color space-based segmentation
* K-means clustering for confident corner selection
* Realtime orientation with edge
* Performs maneuvers in restricted spaces

![Corner detection](https://github.com/Sanidhya-30/rover-docking/blob/main/point_track.gif)

<!--
### Setup and launching the simulation environment:-

* Clone the repo, and build using catkin_make.
```
cd MobileRobot
catkin_make
source ~/{name_of_workspace}/devel/setup.bash
```

* Command `roslaunch mobile_robot test.launch` will launch the gazebo world along 
-->

## Demo Video

![demo video](https://www.youtube.com/watch?v=X0h3elKJ1Yw)


## Prerequisites
* python 3.x
* Raspberry pi
* Pixhawk 
* pyMavlink
