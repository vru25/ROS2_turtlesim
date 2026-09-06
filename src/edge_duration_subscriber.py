import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class EdgeDurationCalculator(Node):

    def __init__(self):
        super().__init__('edge_duration_calculator')

        self.side_length = None
        self.linear_velocity = None

        self.side_length_subscriber = self.create_subscription(
            Float64,
            '/side_length',
            self.side_length_callback,
            10
        )

        self.velocity_subscriber = self.create_subscription(
            Float64,
            '/linear_velocity',
            self.velocity_callback,
            10
        )

        self.duration_publisher = self.create_publisher(
            Float64,
            '/edge_duration',
            10
        )

    def side_length_callback(self, msg):
        self.side_length = msg.data
        self.calculate_duration()

    def velocity_callback(self, msg):
        self.linear_velocity = msg.data
        self.calculate_duration()

    def calculate_duration(self):

        if self.side_length is None:
            return

        if self.linear_velocity is None:
            return

        if self.linear_velocity <= 0.0:
            self.get_logger().warning(
                'Linear velocity must be greater than zero.'
            )
            return

        duration = self.side_length / self.linear_velocity

        msg = Float64()
        msg.data = duration

        self.duration_publisher.publish(msg)

        self.get_logger().info(
            f'Edge duration: {duration:.2f} s '
            f'(side={self.side_length:.2f} m, '
            f'velocity={self.linear_velocity:.2f} m/s)'
        )


def main(args=None):
    rclpy.init(args=args)

    node = EdgeDurationCalculator()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
