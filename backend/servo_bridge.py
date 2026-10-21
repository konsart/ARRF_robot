
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16


class ServoBridge(Node):
    __angle: int

    def __init__(self):
        super().__init__('servo_bridge_node_py')
        self.__angle = 0
        self.publisher_ = self.create_publisher(UInt16, 'servo_bridge', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = UInt16()
        msg.data = self.__angle
        self.publisher_.publish(msg)
        self.__angle = (self.__angle + 1) % 181


def main(args=None):
    rclpy.init(args=args)
    servo_bridge_node = ServoBridge()
    rclpy.spin(servo_bridge_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
