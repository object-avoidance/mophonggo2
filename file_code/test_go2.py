import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import threading

class Go2Controller(Node):
    def __init__(self):
        super().__init__('go2_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.send_cmd)
        
        # Thêm 2 dòng này
        self.linear_x = 0.0
        self.angular_z = 0.0
    # Chạy read_keys ở thread riêng
        self.key_thread = threading.Thread(target=self.read_keys, daemon=True)
        self.key_thread.start()
    def send_cmd(self):
        msg = Twist()
        msg.linear.x = self.linear_x    # đọc từ biến
        msg.angular.z = self.angular_z  # đọc từ biến
        self.pub.publish(msg)
        self.get_logger().info('Sending velocity command')
    def read_keys(self):
        # Cài chế độ đọc từng phím không cần Enter
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while rclpy.ok():
                key = sys.stdin.read(1)  # đọc 1 ký tự

                if key == 'w':
                    self.linear_x = 0.3    # tiến
                    self.angular_z = 0.0
                elif key == 'a':
                    self.linear_x = 0.0
                    self.angular_z = 0.5   # xoay trái
                elif key == 'd':
                    self.linear_x = 0.0
                    self.angular_z = -0.5  # xoay phải
                elif key == 's' or key == ' ':
                    self.linear_x = 0.0    # dừng
                    self.angular_z = 0.0
                elif key == 'x':
                    self.linear_x = -0.3   # lùi
                    self.angular_z = 0.0
                elif key == 'q':
                    break                  # thoát
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)  # restore terminal

def main():
    rclpy.init()
    node = Go2Controller()
    rclpy.spin(node)

if __name__ == '__main__':
    main()