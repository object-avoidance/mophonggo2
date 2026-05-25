#!/bin/bash
echo "Đang kill tất cả process cũ..."
pkill -f gazebo
pkill -f rviz2
pkill -f ros2
pkill -f gzserver
pkill -f gzclient
sleep 3
rm -rf /tmp/launch_params_*
echo "Xong! Chờ 3 giây rồi launch lại..."
ros2 daemon stop && ros2 daemon start
sleep 3
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch unitree_go2_sim unitree_go2_launch.py
