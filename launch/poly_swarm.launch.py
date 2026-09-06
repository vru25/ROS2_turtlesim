#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )

    velocity_server = Node(
        package='ros2_assignment_1',
        executable='polygon_velocity_server.py',
        name='polygon_velocity_server',
        output='screen'
    )

    swarm_manager = Node(
        package='ros2_assignment_1',
        executable='swarm_manager.py',
        name='swarm_manager',
        output='screen'
    )

    spawn_turtle2 = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/spawn',
            'turtlesim/srv/Spawn',
            '{x: 3.0, y: 8.0, theta: 0.0, name: "turtle2"}'
        ],
        output='screen'
    )

    spawn_turtle3 = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/spawn',
            'turtlesim/srv/Spawn',
            '{x: 8.0, y: 3.0, theta: 0.0, name: "turtle3"}'
        ],
        output='screen'
    )

    set_pen_turtle2 = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/turtle2/set_pen',
            'turtlesim/srv/SetPen',
            '{r: 0, g: 255, b: 0, width: 3, off: false}'
        ],
        output='screen'
    )

    set_pen_turtle3 = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/turtle3/set_pen',
            'turtlesim/srv/SetPen',
            '{r: 0, g: 0, b: 255, width: 3, off: false}'
        ],
        output='screen'
    )

    return LaunchDescription([

        turtlesim_node,

        velocity_server,

        TimerAction(
            period=2.0,
            actions=[
                spawn_turtle2
            ]
        ),

        TimerAction(
            period=3.0,
            actions=[
                spawn_turtle3
            ]
        ),

        TimerAction(
            period=4.0,
            actions=[
                set_pen_turtle2,
                set_pen_turtle3
            ]
        ),

        TimerAction(
            period=5.0,
            actions=[
                swarm_manager
            ]
        )
    ])
