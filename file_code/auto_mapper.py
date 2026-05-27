#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class AutoMapper(Node):
    def __init__(self):
        super().__init__('auto_mapper')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        qos = QoSProfile(depth=10)
        qos.reliability = ReliabilityPolicy.BEST_EFFORT

        self.sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, qos)

        self.linear_speed  = 0.4
        self.angular_speed = 0.5
        self.obstacle_dist = 1.2
        self.turn_time     = 2.0
        self.front_dist = 999.0
        self.left_dist  = 999.0
        self.right_dist = 999.0
        self.is_turning = False
        self.turn_start = 0.0
        self.turn_direction = 1.0

        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info('AutoMapper started!')

    def scan_callback(self, msg):
        ranges = msg.ranges
        n = len(ranges)
        if n == 0:
            return

        def safe_range(indices):
            vals = [ranges[i] for i in indices
                    if 0 <= i < n and ranges[i] > 0.05 and ranges[i] == ranges[i]]
            return min(vals) if vals else 999.0

        front_indices = list(range(n//2 - n//12, n//2 + n//12))
        left_indices  = list(range(n//4 - n//12, n//4 + n//12))
        right_indices = list(range(3*n//4 - n//12, 3*n//4 + n//12))

        self.front_dist = safe_range(front_indices)
        self.left_dist  = safe_range(left_indices)
        self.right_dist = safe_range(right_indices)

    def control_loop(self):
        msg = Twist()
        now = time.time()
        if self.is_turning:
            if now - self.turn_start < self.turn_time:
                msg.angular.z = self.angular_speed * self.turn_direction
            else:
                self.is_turning = False
        else:
            if self.front_dist < self.obstacle_dist:
                self.is_turning = True
                self.turn_start = now
                self.turn_direction = 1.0 if self.left_dist > self.right_dist else -1.0
                self.get_logger().info(f'Obstacle! turning...')
            else:
                msg.linear.x  = self.linear_speed
                msg.angular.z = 0.1 * self.turn_direction
        self.pub.publish(msg)

    def stop(self):
        self.pub.publish(Twist())

def main(args=None):
    rclpy.init(args=args)
    node = AutoMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
