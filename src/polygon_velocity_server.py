#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from ros2_assignment_1.srv import ComputePolygonVel


class PolygonVelocityServer(Node):

    def __init__(self):
        super().__init__('polygon_velocity_server')

        self.service = self.create_service(
            ComputePolygonVel,
            'compute_polygon_vel',
            self.compute_velocity
        )

        self.get_logger().info(
            'Polygon velocity service ready: /compute_polygon_vel'
        )

    def compute_velocity(self, request, response):

        n = request.n

        if n < 3:
            self.get_logger().warning(
                'Number of sides must be at least 3.'
            )

            response.linear_velocity = 0.0
            response.angular_velocity = 0.0
            response.turn_duration = 0.0

            return response

        # Constant forward speed for each polygon edge.
        response.linear_velocity = 1.0

        # Constant angular speed during each vertex turn.
        response.angular_velocity = 1.0

        # Exterior turn angle of a regular polygon.
        turn_angle = (2.0 * math.pi) / n

        # Time required to rotate through that angle.
        response.turn_duration = (
            turn_angle / response.angular_velocity
        )

        self.get_logger().info(
            f'N={n} | '
            f'linear velocity={response.linear_velocity:.2f} m/s | '
            f'angular velocity={response.angular_velocity:.2f} rad/s | '
            f'turn duration={response.turn_duration:.4f} s'
        )

        return response


def main(args=None):

    rclpy.init(args=args)

    node = PolygonVelocityServer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
