#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Int32

from ros2_assignment_1.srv import ComputePolygonVel


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.declare_parameter('turtle_name', 'turtle1')
        self.turtle_name = self.get_parameter(
            'turtle_name'
        ).get_parameter_value().string_value

        self.current_n = 3

        self.state = 'WAITING'
        self.side_count = 0

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.turn_duration = 0.0

        self.current_pose = None
        self.edge_start_x = None
        self.edge_start_y = None
        self.turn_start_theta = None

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            f'/{self.turtle_name}/cmd_vel',
            10
        )

        self.sides_subscriber = self.create_subscription(
            Int32,
            '/polygon_sides',
            self.sides_callback,
            10
        )

        self.pose_subscriber = self.create_subscription(
            Pose,
            f'/{self.turtle_name}/pose',
            self.pose_callback,
            10
        )

        self.velocity_client = self.create_client(
            ComputePolygonVel,
            'compute_polygon_vel'
        )

        self.control_timer = self.create_timer(
            0.02,
            self.control_loop
        )

        self.get_logger().info(
            f'Turtle controller started for {self.turtle_name}.'
        )

    def sides_callback(self, msg):
        new_n = msg.data

        if new_n < 3:
            return

        if new_n == self.current_n and self.state != 'WAITING':
            return

        self.current_n = new_n

        self.stop_turtle()
        self.side_count = 0
        self.state = 'WAITING'

        self.request_velocity()

    def pose_callback(self, msg):
        self.current_pose = msg

    def request_velocity(self):
        if not self.velocity_client.service_is_ready():
            return

        request = ComputePolygonVel.Request()
        request.n = self.current_n

        future = self.velocity_client.call_async(request)

        future.add_done_callback(
            self.velocity_response_callback
        )

        self.state = 'REQUESTED'

    def velocity_response_callback(self, future):
        try:
            response = future.result()
        except Exception:
            self.state = 'WAITING'
            return

        self.linear_velocity = response.linear_velocity
        self.angular_velocity = response.angular_velocity
        self.turn_duration = response.turn_duration

        self.side_count = 0

        if self.current_pose is None:
            self.state = 'WAITING'
            return

        self.edge_start_x = self.current_pose.x
        self.edge_start_y = self.current_pose.y

        self.state = 'MOVING'

        self.get_logger().info(
            f'{self.turtle_name}: '
            f'N={self.current_n}, '
            f'v={self.linear_velocity:.2f}, '
            f'omega={self.angular_velocity:.2f}'
        )

    def control_loop(self):

        if self.state == 'WAITING':

            self.stop_turtle()

            if self.velocity_client.service_is_ready():
                self.request_velocity()

            return

        if self.state == 'REQUESTED':

            self.stop_turtle()

            return

        if self.current_pose is None:
            self.stop_turtle()
            return

        if self.state == 'MOVING':

            dx = self.current_pose.x - self.edge_start_x
            dy = self.current_pose.y - self.edge_start_y

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            if distance < 2.0:

                twist = Twist()
                twist.linear.x = self.linear_velocity
                twist.angular.z = 0.0

                self.cmd_vel_publisher.publish(twist)

            else:

                self.stop_turtle()

                self.turn_start_theta = self.current_pose.theta

                self.state = 'TURNING'

        elif self.state == 'TURNING':

            angle_turned = (
                self.current_pose.theta -
                self.turn_start_theta
            )

            while angle_turned < 0.0:
                angle_turned += 2.0 * math.pi

            target_angle = (
                2.0 * math.pi
            ) / self.current_n

            if angle_turned < target_angle:

                twist = Twist()
                twist.linear.x = 0.0
                twist.angular.z = self.angular_velocity

                self.cmd_vel_publisher.publish(twist)

            else:

                self.stop_turtle()

                self.side_count += 1

                if self.side_count >= self.current_n:
                    self.side_count = 0

                self.edge_start_x = self.current_pose.x
                self.edge_start_y = self.current_pose.y

                self.state = 'MOVING'

    def stop_turtle(self):

        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0

        self.cmd_vel_publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()

    rclpy.spin(node)

    node.stop_turtle()
    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
