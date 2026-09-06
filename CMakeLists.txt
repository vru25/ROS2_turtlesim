cmake_minimum_required(VERSION 3.8)
project(ros2_assignment_1)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/PolygonGeometry.srv"
  "srv/ComputePolygonVel.srv"
)

install(
  PROGRAMS
    src/side_length_publisher.py
    src/linear_velocity_publisher.py
    src/edge_duration_subscriber.py
    src/geometry_server.py
    src/geometry_client.py
    src/polygon_sides_publisher.py
    src/polygon_velocity_server.py
    src/turtle_controller.py
    src/swarm_manager.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
