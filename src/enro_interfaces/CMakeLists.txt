cmake_minimum_required(VERSION 3.8)
project(enro_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate the Python and C++ code for our custom service type
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/UzaklikKontrol.srv"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
