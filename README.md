# AutonomousSystem_Project2 @ University of California, Irvine
This project has two parts:
  - Part 1 : Mapping using Hector SLAM - manual control
    - In this problem, I'm going to use TurtleBot3 simulator to build a map for the environment. I manually move the robot until the robot build the map. First, install theHector SLAM package as follows:
    ```
    sudo apt-get install ros-melodic-hector-mapping
    ```
    - Now, in three different terminals, launch the following launch files:
    ```
    roslaunch turtlebot3_gazebo turtlebot3_stage_4.launch
    roslaunch turtlebot3_slam turtlebot3_slam.launchslam_methods:=hector
    roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
    ```
    - Using the keyboard to move the robot around the environment. Observe the map that is beingupdated by the Hector SLAM node. Continue to drive the robot manually until the whole map isbuilt. Once the map is ready, save the map using the map_server node as follows:
    ```
    rosrun map_server map_saver -f ~/map
    ``` 
  - Part 2 : Automatic mapping using Hector SLAM - automatic control
    - In this part, I write a node called **build_map_automatic** that drivesthe robot in the environment to build its map. The node will subscribe to the following topics:
      - **/scan** : this topic contains the information from the LiDAR scanner
      - **/slam_out_pose** : this topic contains the “estimated” pose of the robot from thelocalization algorithm
      - **/map** : this topic contains the occupancy map estimated by the SLAM algorithm <br />
    - This node should then publish to the topic:
      - **/cmd_vel** : this topic is used to control the linear and the angular velocities of the robot. <br />
    - This node should perform the following steps:
      1. Read the current occupancy map. Determine if more areas of the map need to beexplored.
      2. Pick a point that is on the edge of what is currently explored. Move the robot to that point. Make sure the robot does not hit an obstacle while it moves to that point (you will need the LiDAR information to correct the course of the robot to avoid hitting the obstacles).
      3. Repeat steps 1 and 2 until the whole map is obtained. Save the map and printout thetime used to build the map.
