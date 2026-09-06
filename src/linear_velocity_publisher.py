import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class LinearVelocityPublisher(Node):

    def __init__(self):
        super().__init__('linear_velocity_publisher')

        self.publisher = self.create_publisher(
            Float64,
            '/linear_velocity',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_linear_velocity
        )

        self.linear_velocity = 1.0

    def publish_linear_velocity(self):
        msg = Float64()
        msg.data = self.linear_velocity

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing linear velocity: {msg.data:.2f} m/s'
        )


def main(args=None):
    rclpy.init(args=args)

    node = LinearVelocityPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
