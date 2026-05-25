import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Go2Controller(Node):
    def __init__(self):
        super().__init__('go2_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # Gửi lệnh mỗi 0.5 giây
        self.timer = self.create_timer(0.5, self.send_cmd)

    def send_cmd(self):
        msg = Twist()
        msg.linear.x = 0.3   # tiến 0.3 m/s
        msg.angular.z = 0.0  # không xoay
        self.pub.publish(msg)
        self.get_logger().info('Sending velocity command')

def main():
    rclpy.init()
    node = Go2Controller()
    rclpy.spin(node)

if __name__ == '__main__':
    main()