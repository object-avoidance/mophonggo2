from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
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
        }],
        ros_arguments=[
            '--ros-args',
            '--remap', '__node:=pointcloud_to_laserscan',
            '-p', 'qos_overrides./scan.publisher.reliability:=best_effort',
        ]
    )

    slam = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[{
            'use_sim_time':             True,
            'base_frame':              'base_footprint',
            'odom_frame':              'odom',
            'map_frame':               'map',
            'scan_topic':              '/scan',
            'max_laser_range':          15.0,
            'mode':                    'mapping',
            'map_update_interval':      0.5,
            'resolution':               0.05,
            'minimum_travel_distance':  0.1,
            'minimum_travel_heading':   0.1,
        }],
        ros_arguments=[
            '--ros-args',
            '-p', 'qos_overrides./scan.subscription.reliability:=best_effort',
        ]
    )

    return LaunchDescription([
        converter,
        TimerAction(period=3.0, actions=[slam]),
    ])
