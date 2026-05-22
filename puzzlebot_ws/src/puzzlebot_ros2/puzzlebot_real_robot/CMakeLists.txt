cmake_minimum_required(VERSION 3.8)
project(puzzlebot_real_robot)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    launch
    config
    maps
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/puzzlebot_localization.py
    scripts/puzzlebot_joint_state_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()