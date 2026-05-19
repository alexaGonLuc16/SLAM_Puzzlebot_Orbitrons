cmake_minimum_required(VERSION 3.8)
project(puzzlebot_real_robot)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch config maps scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()