#!/usr/bin/env python3

import re
import subprocess

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class SwarmManager(Node):

    def __init__(self):
        super().__init__('swarm_manager')

        self.controllers = {}

        self.sides_publisher = self.create_publisher(
            Int32,
            '/polygon_sides',
            10
        )

        self.monitor_timer = self.create_timer(
            0.5,
            self.monitor_turtles
        )

        self.get_logger().info(
            'Swarm manager started.'
        )

    def monitor_turtles(self):

        services = self.get_service_names_and_types()

        active_turtles = set()

        for service_name, _ in services:

            match = re.match(
                r'^/turtle(\d+)/set_pen$',
                service_name
            )

            if match:
                active_turtles.add(
                    f'turtle{match.group(1)}'
                )

        active_turtles = sorted(
            active_turtles,
            key=lambda name: int(
                name.replace('turtle', '')
            )
        )

        turtle_count = len(active_turtles)

        polygon_sides = max(3, turtle_count)

        msg = Int32()
        msg.data = polygon_sides
        self.sides_publisher.publish(msg)

        for turtle_name in active_turtles:

            if turtle_name not in self.controllers:

                process = subprocess.Popen([
                    'ros2',
                    'run',
                    'ros2_assignment_1',
                    'turtle_controller.py',
                    '--ros-args',
                    '-p',
                    f'turtle_name:={turtle_name}'
                ])

                self.controllers[turtle_name] = process

                self.get_logger().info(
                    f'Controller started for {turtle_name}.'
                )

        for turtle_name in list(self.controllers.keys()):

            if turtle_name not in active_turtles:

                process = self.controllers.pop(
                    turtle_name
                )

                process.terminate()

                self.get_logger().info(
                    f'Controller stopped for {turtle_name}.'
                )

        self.get_logger().info(
            f'Active turtles: {turtle_count} | '
            f'Polygon sides: {polygon_sides}'
        )

    def destroy_node(self):

        for process in self.controllers.values():
            process.terminate()

        self.controllers.clear()

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = SwarmManager()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
