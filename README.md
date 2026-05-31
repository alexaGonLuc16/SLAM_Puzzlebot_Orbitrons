# Puzzlebot Autonomous Navigation using SLAM and AMCL - Orbitrons

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

## Descripción del proyecto
Este proyecto implementa un sistema de mapeo, localización y navegación autónoma para un Puzzlebot utilizando ROS 2. Se emplea SLAM Toolbox para la construcción de mapas del entorno y AMCL (Adaptive Monte Carlo Localization) para la localización del robot sobre los mapas previamente generados. Una vez localizado, el robot utiliza Navigation2 para planificar y ejecutar trayectorias de forma autónoma en entornos reales mediante información proveniente de un sensor LiDAR.

El sistema incluye:
- Modelado del robot
- Simulación en Gazebo
- Algoritmos de navegación

El proyecto está orientado a la implementación en hardware real y permite realizar el ciclo completo de exploración, generación de mapas, localización y navegación autónoma.

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
│   └── puzzlebot_gazebo.launch.xml        
├── package.xml
├── worlds/
    └── maze.world

```
## puzzlebot_navigation2

```text
puzzlebot_navigation2/
├── CMakeLists.txt
├── config/
│   ├── nav2_params.yaml
│   └── slam_toolbox.yaml
├── launch/
│   ├── nav2_core.launch.xml
│   ├── nav2.launch.xml
│   ├── slam_core.launch.xml
│   └── slam.launch.xml
├── maps/
│   ├── MALOmy_map.pgm
│   ├── MALOmy_map.yaml
│   ├── my_map.pgm
│   └── my_map.yaml       
├── package.xml
├── rviz/
│   ├── nav2.rviz
|   └── slam.rviz
└── scripts

```
