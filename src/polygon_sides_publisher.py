#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class PolygonSidesPublisher(Node):

    def __init__(self):
        super().__init__('polygon_sides_publisher')

        self.publisher = self.create_publisher(
            Int32,
            '/polygon_sides',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_sides
        )

        self.sides = 3

    def publish_sides(self):
        msg = Int32()
        msg.data = self.sides

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing polygon sides: {self.sides}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = PolygonSidesPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
