roboURDF - Gazebo Harmonic Simulation

This project contains a 6-wheeled robot URDF and simulation environment for ROS 2 Humble and Gazebo Harmonic.

Prerequisites

Ensure you have the Gazebo Harmonic and the ROS-GZ bridge installed:

    sudo apt update
    sudo apt install ros-humble-ros-gz


1. Terminal 1: Build and Launch Simulation

Launch the robot state publisher and the Gazebo simulator.

    cd ~/ros2_ws
    colcon build --symlink-install --packages-select roboURDF
    source install/setup.bash
    ros2 launch roboURDF launch_sim.launch.py


2. Terminal 2: Start the ROS-GZ Bridge (MANDATORY)

Because Gazebo Harmonic is decoupled from ROS, this bridge translates the messages between the two.

# This maps velocity, odometry, and transforms
    ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist /odom@nav_msgs/msg/Odometry@gz.msgs.Odometry /tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V


3. Terminal 3: Teleop Control

Run the keyboard controller to move the robot.

    cd ~/ros2_ws
    source install/setup.bash
    ros2 run roboURDF arrow_teleop.py


Key Controls

Up Arrow: Forward

Down Arrow: Backward

Left Arrow: Spin Left

Right Arrow: Spin Right

'q': Quit controller

Troubleshooting

If the robot does not move:

Ensure the Bridge (Terminal 2) is running and shows no errors.

Ensure you have updated your URDF to use the gz-sim-diff-drive-system plugin instead of the old Gazebo Classic libgazebo_ros_diff_drive.so.

Check that your package name in package.xml and CMakeLists.txt is exactly roboURDF.