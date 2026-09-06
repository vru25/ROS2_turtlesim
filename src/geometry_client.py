#!/usr/bin/env python3

import sys

import rclpy
from rclpy.node import Node

from ros2_assignment_1.srv import PolygonGeometry


class GeometryClient(Node):

    def __init__(self):
        super().__init__('geometry_client')

        self.client = self.create_client(
            PolygonGeometry,
            'compute_polygon_geometry'
        )

    def send_request(self, n, l):

        if not self.client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error(
                'Geometry service is not available.'
            )
            return False

        request = PolygonGeometry.Request()
        request.n = n
        request.l = l

        future = self.client.call_async(request)

        self.get_logger().info(
            'Sending geometry request...'
        )

        rclpy.spin_until_future_complete(
            self,
            future,
            timeout_sec=3.0
        )

        if not future.done():
            self.get_logger().error(
                'Service request timed out after 3 seconds.'
            )
            return False

        if future.exception() is not None:
            self.get_logger().error(
                f'Service call failed: {future.exception()}'
            )
            return False

        response = future.result()

        self.get_logger().info(
            f'Exterior turn angle: '
            f'{response.exterior_angle:.4f} rad'
        )

        self.get_logger().info(
            f'Total perimeter: '
            f'{response.perimeter:.2f}'
        )

        return True


def main(args=None):

    rclpy.init(args=args)

    node = GeometryClient()

    n = 4
    l = 2.0

    if len(sys.argv) >= 2:
        n = int(sys.argv[1])

    if len(sys.argv) >= 3:
        l = float(sys.argv[2])

    node.get_logger().info(
        f'Request: N={n}, L={l:.2f}'
    )

    node.send_request(n, l)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
