
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16


class ServoBridge(Node):
    def __init__(self) -> None:
        super().__init__('servo_bridge_node_py')
        
        self.publisher_ = self.create_publisher(UInt16, 'servo_bridge', 10)
        self.subscriber_ = self.create_subscription(UInt16, 'servo/cmd_angle', self.callback, 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.__angle = 0

    def callback(self, msg: UInt16) -> None:
        self.get_logger().info('Got angle: %' % msg.data)

    def timer_callback(self) -> None:
        msg = UInt16()
        msg.data = self.__angle
        self.publisher_.publish(msg)
        self.__angle = (self.__angle + 1) % 181


def main(args=None):
    rclpy.init(args=args)
    servo_bridge_node = ServoBridge()
    try:
        rclpy.spin(servo_bridge_node)
    except KeyboardInterrupt:
        pass
    finally:
        servo_bridge_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
