# ROS 2 Research Notes

Alpar Garib, ENRO software team candidate assignment

## ROS 2: what is it and why is it used?

ROS 2 (Robot Operating System 2) is not an operating system. It is a set of libraries and tools that runs on top of Linux and lets robot software communicate. A robot's software is not one large program, but many small programs that exchange data, even across different computers. ROS 2 handles this communication through DDS.

Robots need the same basic systems: sensor drivers, logging, visualization (RViz), simulation (Gazebo) and navigation. ROS 2 lets us reuse these tools instead of building them again, and parts written in C++ (rclcpp) and Python (rclpy) work together. Unlike ROS 1, it has no central master: nodes find each other on their own. Jazzy Jalisco is the LTS release for Ubuntu 24.04.

## Workspace, package and node

- **Workspace:** the folder where we develop, like `~/ros2_ws`. The code goes into `src/`, and `colcon build` creates `build/`, `install/` and `log/`. After building, `source install/setup.bash` makes our packages visible to ROS.
- **Package:** the unit that organizes code. Every package has a `package.xml` with its name, version and dependencies. Interface and C++ packages use `CMakeLists.txt`; Python packages use `setup.py` and `setup.cfg`.
- **Node:** one running program with one job, like a camera driver or a distance calculator. Nodes communicate through topics, services and actions.

## Topic, message, publisher and subscriber

A **topic** is a named channel, like `/enro/hedef_uzakligi`. A **publisher** sends data to it, and a **subscriber** receives data from it. The data is sent as a **message**, a type with fixed fields: `std_msgs/msg/Float64` has one field called `data`. Both sides must use the same type, but they don't need to know about each other. A topic can have many publishers and subscribers. Topics are one-way, so they are useful for data that keeps coming, like sensor readings.

## Service, client, request and response

A **service** is a question and an answer. The **server** offers the service, and a **client** sends a **request** and receives one **response**. A `.srv` file defines both: request fields above `---`, response fields below it. There can be many clients, but a service name should have only one server. Services are for short operations, like a calculation, not for long tasks, because the client waits until the answer comes.

## Action, goal, feedback and result

An **action** is for long tasks. The client sends a **goal**, the server accepts or rejects it, sends **feedback** during the task, and sends a **result** at the end. The client can also cancel the goal. For example, in "walk to point (5, 3)", the feedback is the remaining distance and the result is whether the robot arrived. Actions are built on top of topics and services.

## Parameter, launch and ros2 commands

- **Parameter:** a setting of a node, like a speed limit. It can be set at startup or changed while the node runs, without changing the code.
- **Launch:** a launch file (Python, XML or YAML) starts many nodes at once with their settings. A real robot has too many nodes to start one by one. It runs with `ros2 launch <package> <file>`.
- **ros2 commands:** command line tools for testing a running system without writing extra code, like `ros2 run`, `ros2 node list`, `ros2 topic echo`, `ros2 service call`, `ros2 action send_goal`, `ros2 param set` and `ros2 interface show`.

## Topic vs service vs action

| | Topic | Service | Action |
|---|---|---|---|
| Communication | one-way, continuous | one request, one response | goal, feedback, result |
| Can be cancelled | no | no | yes |
| Use | data that keeps coming | short questions | long tasks |
| Robot dog example | the IMU publishes the body angle | "how far is the target, and is it closer than 5 m?" | "walk to the target", with the remaining distance as feedback |
