#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from ros2_assignment_1.srv import PolygonGeometry


class GeometryServer(Node):

    def __init__(self):
        super().__init__('geometry_server')

        self.service = self.create_service(
            PolygonGeometry,
            'compute_polygon_geometry',
            self.calculate_geometry
        )

        self.get_logger().info(
            'Geometry service ready: /compute_polygon_geometry'
        )

    def calculate_geometry(self, request, response):

        n = request.n
        l = request.l

        if n < 3:
            self.get_logger().warning(
                'Number of sides must be at least 3.'
            )
            response.exterior_angle = 0.0
            response.perimeter = 0.0
            return response

        if l <= 0.0:
            self.get_logger().warning(
                'Side length must be greater than zero.'
            )
            response.exterior_angle = 0.0
            response.perimeter = 0.0
            return response

        response.exterior_angle = (2.0 * math.pi) / n
        response.perimeter = n * l

        self.get_logger().info(
            f'N={n}, L={l:.2f} | '
            f'exterior angle={response.exterior_angle:.4f} rad | '
            f'perimeter={response.perimeter:.2f}'
        )

        return response


def main(args=None):
    rclpy.init(args=args)

    node = GeometryServer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
