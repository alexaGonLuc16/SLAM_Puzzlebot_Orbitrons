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
- Modelado del robot mediante URDF/Xacro
- Generación de mapas utilizando SLAM Toolbox y un sensor LiDAR
- Localización probabilística mediante AMCL
- Navegación autónoma utilizando Navigation2
- Publicación y gestión de transformaciones TF
- Planificación y seguimiento de trayectorias en tiempo real

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

Este paquete contiene la descripción completa del robot utilizando URDF/Xacro. Define la estructura mecánica del Puzzlebot, los sensores, los frames TF, las propiedades físicas y los modelos visuales utilizados por RViz y ROS 2.

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
    ├── puzzlebot_physical.urdf.xacro
    └── rpi_lidar_sensor.xacro
```
- `puzzlebot.urdf.xacro`:
Es el archivo encargado de ensamblar el robot completo.

- `puzzlebot_base.urdf.xacro`:
Define chasis, ruedas, caster wheel y joints.

- `puzzlebot_control.xacro`:
Define control diferencial, odometría e interfaces de ROS2.

- `puzzlebot_physical.urdf.xacro`:
Una versión adaptada para el robot físico.

- `rpi_lidar_sensor.xacro`:
Define el frame del LiDAR, el sensor láser y la publicación de /scan.

- `puzzlebot_description.launch.xml`:
Lanza robot_state_publisher y publica TF.

## puzzlebot_gazebo

Paquete utilizado durante la fase de simulación. Permite ejecutar el Puzzlebot dentro de Gazebo, simular sensores y validar algoritmos antes de desplegarlos en hardware real.

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
- `maze.world`:
Es el entorno de simulación que contiene las paredes, los obstáculos y en general la geometría del laberinto.
- `gazebo_bridge.yaml`:
Es la conexión entre ROS2 y Gazebo. 
- `puzzlebot_gazebo.launch.xml`:
Lanza Gazebo, el mundo y robot virtuales.

## puzzlebot_navigation2

Paquete encargado del mapeo y navegación utilizando las herramientas estándar de ROS2 Navigation Stack.

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
- `slam.launch.xml`:
Lanza el entorno para crear mapas.
- `slam_core.launch.xml`:
Ejecuta los nodos necesarios para SLAM.
- `nav2.launch.xml`:
Lanza Navigation2 completo.
- `nav2_core.launch.xml`:
Configura los nodos internos de Nav2.
- `slam_toolbox.yaml`:
Configuración de optimización del mapa.
- `nav2_params.yaml`:
Configuración de AMCL, Planner, Controller, Costmaps y Recovery Behaviors.
- `slam.rviz`:
Visualización del proceso de mapeo.
- `nav2.rviz`:
Visualización durante la navegación.

## puzzlebot_real_robot

Este paquete integra el robot físico con ROS2.

```text
puzzlebot_real_robot/
│
├── scripts/
│   ├── puzzlebot_joint_state_publisher.py
│   └── puzzlebot_localization.py
│
├── config/
│   ├── nav2_params_real.yaml
│   └── slam_toolbox_real.yaml
│
├── launch/
│   ├── slam_real.launch.xml
│   ├── nav2_real.launch.xml
│   └── real_robot_core.launch.xml
│
└── maps/
    ├── map_maze_real.*
    └── OTROmap_maze_real.*
```
- `puzzlebot_joint_state_publisher.py`:
Publica /joint_states y permite actualizar los valores de las ruedas en base_link.
- `puzzlebot_localization.py`:
Nodo de localización del robot.
- `slam_real.launch.xml`:
Lanza SLAM Toolbox sobre el robot físico.
- `nav2_real.launch.xml`:
Lanza Navigation2 para navegación autónoma.
- `real_robot_core.launch.xml`:
Lanza los nodos base necesarios para el robot real.
- `slam_toolbox_real.yaml`:
Parámetros específicos del LiDAR y del entorno real.
- `nav2_params_real.yaml`:
Parámetros optimizados.
