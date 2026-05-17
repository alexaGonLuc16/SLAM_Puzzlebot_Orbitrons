# Puzzlebot - Orbitrons

- **Grupo:** 502  
- **Equipo:** Orbitrons  

## Integrantes
| Nombre | Matrícula |
|--------|----------|
| Alexa Jimena González Lucio | A01277701 |
| Mario Godínez Chavero | A01710451 |
| Paul Park | A01709885 |
| Sebastián Castellanos Rodríguez | A01710226 |

---

## Descripción del Proyecto
Este proyecto consiste en la implementación de un robot tipo *Puzzlebot* utilizando ROS 2, enfocado en navegación autónoma y simulación en entornos virtuales.

El sistema incluye:
- Modelado del robot
- Simulación en Gazebo
- Algoritmos de navegación

---

## Estructura del Proyecto

```bash
puzzlebot_ws/
└── src/
    └── puzzlebot_ros2/
        ├── puzzlebot_description/
        ├── puzzlebot_gazebo/
        └── puzzlebot_navigation/
```
## puzzlebot_description

```text
puzzlebot_description/
├── CMakeLists.txt
├── launch/
│   └── puzzlebot_description.launch.xml
├── meshes/
│   ├── MCR2_puzzlebot_jetson_lidar_base.stl        
│   ├── Puzzlebot_Caster_Wheel.stl     
│   ├── Puzzlebot_Jetson_Lidar_Edition_Base(1).stl
│   ├── Puzzlebot_Wheel.stl
│   └── RPLidar.stl
├── package.xml
├── rviz/
│   └── puzzlebot_description.rviz
└── urdf/
    ├── puzzlebot_base.urdf.xacro
    ├── puzzlebot_control.xacro
    ├── puzzlebot.urdf.xacro
    ├── puzzlebot.xacro
    └── rpi_lidar_sensor.xacro
```

## puzzlebot_gazebo

```text
puzzlebot_gazebo/
├── CMakeLists.txt
├── config/
│   └── gazebo_bridge.yaml
├── launch/
│   ├── puzzlebot_gazebo.launch.xml        
├── package.xml
├── worlds/
    └── maze.world

```
