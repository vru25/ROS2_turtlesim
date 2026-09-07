# ROS 2 Turtlesim Polygon Swarm

A complete ROS 2 implementation for publisher-subscriber communication, custom services, automated polygon drawing in turtlesim, and dynamic multi-turtle polygon scaling.

The project was developed and tested in a local ROS 2 Humble environment running on WSL Ubuntu.

---

## Overview

This assignment demonstrates several fundamental ROS 2 concepts through a progressively developed polygon-drawing system:

1. Publisher–Subscriber communication
2. Client–Service communication using custom ROS 2 interfaces
3. Automated regular polygon drawing using turtlesim
4. Multi-turtle swarm control
5. Dynamic polygon scaling based on the number of active turtles
6. Dynamic despawn handling
7. rosbag2 recording and playback data

The final system allows multiple turtles to continuously draw regular polygons while automatically changing the polygon based on the number of active turtles.

### Dynamic behaviour

| Active Turtles | Polygon |
|---------------|---------|
| 3 | Triangle |
| 4 | Square |
| 5 | Pentagon |

When a turtle is removed, the remaining turtles automatically step back to the appropriate polygon.

---

# Project Structure

```text
ROS2_turtlesim/
│
├── CMakeLists.txt
├── package.xml
├── README.md
│
├── launch/
│   └── poly_swarm.launch.py
│
├── src/
│   ├── side_length_publisher.py
│   ├── linear_velocity_publisher.py
│   ├── edge_duration_subscriber.py
│   ├── geometry_server.py
│   ├── geometry_client.py
│   ├── polygon_sides_publisher.py
│   ├── polygon_velocity_server.py
│   ├── turtle_controller.py
│   └── swarm_manager.py
│
├── srv/
│   ├── PolygonGeometry.srv
│   └── ComputePolygonVel.srv
│
├── rosbag2/
│   ├── metadata.yaml
│   └── rosbag2_2026_09_06-20_28_14_0.db3
│
├── resource/
│   └── ros2_assignment_1
│
├── ros2_assignment_1/
│   └── __init__.py
│
└── test/
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py
