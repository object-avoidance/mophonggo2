# mophonggo2
#!/bin/bash
# setup.sh — chạy file này để setup môi trường từ đầu
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone https://github.com/RobInLabUJI/unitree_go2_ros2_jazzy
git clone https://github.com/unitreerobotics/unitree_ros

# Clone repo của bạn
git clone https://github.com/<your_username>/my_go2_project

cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
echo "Setup xong!"
