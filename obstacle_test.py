import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class ObstacleReader(Node):
    def __init__(self):
        super().__init__('obstacle_reader')
        self.sub = self.create_subscription(
            PointCloud2,
            '/unitree_lidar/points',  # topic LiDAR của bạn
            self.lidar_callback,
            10
        )
        self.get_logger().info('Đang lắng nghe LiDAR...')

    def lidar_callback(self, msg):
        points = list(pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True))
        self.get_logger().info(f'Nhận được {len(points)} điểm | '
                               f'Ví dụ điểm đầu: {points[0] if points else "trống"}')

def main():
    rclpy.init()
    rclpy.spin(ObstacleReader())

if __name__ == '__main__':
    main()