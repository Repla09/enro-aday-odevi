# ENRO target distance check service

A small ROS 2 Jazzy program that calculates how far the ENRO robot dog is from a target and whether it is within a given proximity threshold. It does not move the robot.

Alpar Garib, ENRO software team candidate assignment

## How it works

1. **The client** (`uzaklik_istemci`) takes five numbers from the command line: `robot_x robot_y hedef_x hedef_y yakinlik_esigi_m` (positions and threshold in meters). It sends them as a request to the `/enro/uzaklik_kontrol` service and prints the response.
2. **The server** (`uzaklik_sunucu`) checks the request:
   - If any value is not a finite number (`nan`, `inf`) or the threshold is 0 or negative, it answers `basarili = false`, `uzaklik_m = 0`, `hedefe_yakin = false` with an error message in `aciklama`, and **does not publish** anything.
   - Otherwise it calculates `dx = hedef_x - robot_x`, `dy = hedef_y - robot_y`, `uzaklik = sqrt(dx² + dy²)`, and sets `hedefe_yakin = true` if the distance is less than or equal to the threshold.
3. For every successful request, the server also **publishes the distance once** on the `/enro/hedef_uzakligi` topic (`std_msgs/msg/Float64`).

## Packages

```
ros2_ws/
  README.md
  ARASTIRMA.md                 ROS 2 research notes
  .gitignore                   keeps build/, install/ and log/ out of the repo
  src/
    enro_interfaces/           custom service type (ament_cmake)
      srv/UzaklikKontrol.srv
      CMakeLists.txt
      package.xml
    enro_uzaklik/              Python nodes (ament_python)
      enro_uzaklik/
        __init__.py
        uzaklik_sunucu.py      service server + topic publisher
        uzaklik_istemci.py     client that sends one request
      package.xml
      setup.py                 entry points for the two nodes
      setup.cfg
      resource/enro_uzaklik
```

Service `/enro/uzaklik_kontrol`, type `enro_interfaces/srv/UzaklikKontrol`:

```
float64 robot_x
float64 robot_y
float64 hedef_x
float64 hedef_y
float64 yakinlik_esigi_m
---
bool basarili
float64 uzaklik_m
bool hedefe_yakin
string aciklama
```

## Build

Requirements: Ubuntu 24.04 with ROS 2 Jazzy (Desktop) and the ROS development tools.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Run

Terminal 1, start the server:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run enro_uzaklik uzaklik_sunucu
```

Terminal 2, watch the topic:

```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /enro/hedef_uzakligi
```

Terminal 3, send the five example requests:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run enro_uzaklik uzaklik_istemci 0 0 3 4 5
ros2 run enro_uzaklik uzaklik_istemci 0 0 3 4 4
ros2 run enro_uzaklik uzaklik_istemci 2 3 2 3 1
ros2 run enro_uzaklik uzaklik_istemci -1 -1 2 3 5
ros2 run enro_uzaklik uzaklik_istemci 0 0 1 1 0
```

The service can also be called without the client:

```bash
ros2 service call /enro/uzaklik_kontrol enro_interfaces/srv/UzaklikKontrol \
  "{robot_x: 0.0, robot_y: 0.0, hedef_x: 3.0, hedef_y: 4.0, yakinlik_esigi_m: 5.0}"
```

## Results

Service responses printed by the client:

| Robot (x, y) | Target (x, y) | Threshold | Response |
|---|---|---|---|
| (0, 0) | (3, 4) | 5 m | `basarili=True, uzaklik_m=5.0, hedefe_yakin=True, aciklama="Target is within the threshold (5.00 m <= 5.00 m)"` |
| (0, 0) | (3, 4) | 4 m | `basarili=True, uzaklik_m=5.0, hedefe_yakin=False, aciklama="Target is outside the threshold (5.00 m > 4.00 m)"` |
| (2, 3) | (2, 3) | 1 m | `basarili=True, uzaklik_m=0.0, hedefe_yakin=True, aciklama="Target is within the threshold (0.00 m <= 1.00 m)"` |
| (-1, -1) | (2, 3) | 5 m | `basarili=True, uzaklik_m=5.0, hedefe_yakin=True, aciklama="Target is within the threshold (5.00 m <= 5.00 m)"` |
| (0, 0) | (1, 1) | 0 m | `basarili=False, uzaklik_m=0.0, hedefe_yakin=False, aciklama="Error: yakinlik_esigi_m must be greater than 0"` |

Topic output (`ros2 topic echo /enro/hedef_uzakligi`) for the four successful requests:

```
data: 5.0
---
data: 5.0
---
data: 0.0
---
data: 5.0
---
```

The fifth request is invalid (threshold 0), so the server only returns the error and **nothing is published** on the topic. The same happens for non-finite inputs, for example `ros2 run enro_uzaklik uzaklik_istemci 0 0 nan 1 5` returns `Error: all values must be finite numbers`.
