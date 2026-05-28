from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    unitree_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('unitree_go2_sim'),
                'launch', 'unitree_go2_launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'true'}.items(),
    )

    converter = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[('cloud_in', '/velodyne_points/points')],
        parameters=[{
            'min_height':   -2.0,
            'max_height':    2.0,
            'range_min':     0.1,
            'range_max':    20.0,
            'target_frame': 'base_footprint',
            'use_sim_time':  True,
        }]
    )

    slam = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[{
            'use_sim_time':            True,
            'base_frame':             'base_footprint',
            'odom_frame':             'odom',
            'map_frame':              'map',
            'scan_topic':             '/scan',
            'max_laser_range':         15.0,
            'mode':                   'mapping',
            'map_update_interval':     0.5,
            'resolution':              0.05,
            'minimum_travel_distance': 0.1,
            'minimum_travel_heading':  0.1,
        }]
    )

    return LaunchDescription([
        unitree_sim,
        TimerAction(period=5.0,  actions=[converter]),
        TimerAction(period=8.0,  actions=[slam]),
        TimerAction(period=12.0, actions=[
            ExecuteProcess(
                cmd=['ros2', 'lifecycle', 'set', '/slam_toolbox', 'configure'],
                output='screen'
            )
        ]),
        TimerAction(period=15.0, actions=[
            ExecuteProcess(
                cmd=['ros2', 'lifecycle', 'set', '/slam_toolbox', 'activate'],
                output='screen'
            )
        ]),
    ])
