import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np
import time

class PointCloudFast(Node):
    def __init__(self):
        super().__init__('pointcloud_fast')
        self.sub = self.create_subscription(
            PointCloud2,
            '/unitree_lidar/points',
            self.callback,
            10
        )

    def callback(self, msg):
        t0 = time.perf_counter()

        # Đọc thành numpy array thay vì list
        points = np.frombuffer(msg.data, dtype=np.float32).reshape(-1, 5)
        # Cột: 0=x, 1=y, 2=z, 3=intensity, 4=ring (dạng float32 raw)

        t1 = time.perf_counter()

        # Lọc finite bằng numpy — vectorized, không loop
        mask = np.isfinite(points[:, 0]) & \
               np.isfinite(points[:, 1]) & \
               np.isfinite(points[:, 2])
        valid = points[mask]

        t2 = time.perf_counter()

        # Tách các cột
        xyz       = valid[:, :3]
        intensity = valid[:, 3]
        ring      = valid[:, 4].astype(int)

        t3 = time.perf_counter()

        self.get_logger().info(
            f'\n Tổng: {len(points)} | Hợp lệ: {len(valid)} '
            f'({len(valid)/len(points)*100:.1f}%)'
            f'\n frombuffer : {(t1-t0)*1000:.2f} ms'
            f'\n lọc numpy  : {(t2-t1)*1000:.2f} ms'
            f'\n tách cột   : {(t3-t2)*1000:.2f} ms'
            f'\n Tổng       : {(t3-t0)*1000:.2f} ms'
        )

def main():
    rclpy.init()
    rclpy.spin(PointCloudFast())

if __name__ == '__main__':
    main()