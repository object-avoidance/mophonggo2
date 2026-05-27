from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[('cloud_in', '/unitree_lidar/points')],
            parameters=[{
                'use_sim_time': True,
                'min_height': -0.3,
                'max_height': 0.3,
                'range_min': 0.1,
                'range_max': 15.0,
                'angle_min': -3.14159,
                'angle_max': 3.14159,
            }]
        ),
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[{
                'use_sim_time': True,
                'scan_topic': '/scan',
                'odom_frame': 'odom',
                'map_frame': 'map',
                'base_frame': 'base_footprint',
                'mode': 'mapping',
                'resolution': 0.05,
            }]
        ),
    ])
