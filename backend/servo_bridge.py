#!/usr/bin/env python3
# exit codes: 0=ok, 1=Ctrl+C, 3=serial connection loss / boot no-port

import sys
from serial import Serial, SerialException

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16


OK_EC = 0x0
KEYBOARD_EC = 0x1
SERIAL_CON_EC = 0x3


class ServoBridge(Node):
    def __init__(self) -> None:
        super().__init__('servo_bridge_node')

        self.port = '/dev/ttyACM0'
        try:
            self.ser = Serial(self.port, 115200)
        except SerialException:
            self.get_logger().info('Port not found')
            sys.exit(SERIAL_CON_EC)
        self._sbuf = b''
        
        self.publisher_ = self.create_publisher(UInt16, 'servo/current_angle', 10)
        self.subscriber_ = self.create_subscription(UInt16, 'servo/cmd_angle', self.callback, 10)
        self.timer = self.create_timer(0.05, self.timer_callback)

    def callback(self, msg: UInt16) -> None:
        self.get_logger().debug('Got angle: %d' % msg.data)
        self.ser.write(b'set_angle:%d\n' % min(msg.data, 180))

    def timer_callback(self) -> None:
        self._sbuf += self.ser.read(self.ser.in_waiting)

        while (nl_ind := self._sbuf.find(b'\n')) != -1:
            msg = self._sbuf[:nl_ind].strip()
            self._sbuf = self._sbuf[nl_ind+1:]

            if (sep_ind := msg.find(b':')) == -1: continue
            if msg[:sep_ind] != b'angle': continue
            if not (data := msg[sep_ind+1:]).isdigit(): continue

            self.publisher_.publish(UInt16(data=int(data)))


def main(args=None) -> None:
    rclpy.init(args=args)
    servo_bridge_node = ServoBridge()
    exit_code = OK_EC
    try:
        rclpy.spin(servo_bridge_node)
    except KeyboardInterrupt:
        servo_bridge_node.ser.close()
        servo_bridge_node.get_logger().info("Keyboard interrupt")
        exit_code = KEYBOARD_EC
    except SerialException:
        servo_bridge_node.get_logger().info("Port connection lost")
        exit_code = SERIAL_CON_EC
    finally:
        servo_bridge_node.destroy_node()
        rclpy.shutdown()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
