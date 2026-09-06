import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class SideLengthPublisher(Node):

    def __init__(self):
        super().__init__('side_length_publisher')

        self.publisher = self.create_publisher(
            Float64,
            '/side_length',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_side_length
        )

        self.side_length = 2.0

    def publish_side_length(self):
        msg = Float64()
        msg.data = self.side_length

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing side length: {msg.data:.2f} m'
        )


def main(args=None):
    rclpy.init(args=args)

    node = SideLengthPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
