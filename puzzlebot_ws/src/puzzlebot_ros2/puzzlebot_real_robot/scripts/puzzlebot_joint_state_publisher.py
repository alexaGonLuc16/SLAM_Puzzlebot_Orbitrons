#!/usr/bin/env python3
# Librerias
import rclpy 
from rclpy.node import Node 
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry


class StatePublisher(Node):
    def __init__(self):
        super().__init__('puzzlebot_joint_state_publisher')

        # Parámetros del robot
        self.r = 0.05 # wheel radius
        self.L = 0.19 # wheelbase

        # Velocidades de odom
        self.v = 0.0
        self.w = 0.0

        # Posición de las llantas
        self.left_wheel_pos = 0.0
        self.right_wheel_pos = 0.0

        self.dt = 0.05

        # SUBSCRIBER
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_cb, 10)

        # PUBLISHERS
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

        # Creo el mensaje Joint
        self.joints = JointState()
        self.joints.name = ['wheel_l_joint', 'wheel_r_joint']
        self.joints.position = [0.0, 0.0]
        self.joints.velocity = [0.0, 0.0]
        self.joints.effort = [0.0, 0.0]

        # Timer
        self.timer = self.create_timer(self.dt, self.timer_cb)

        self.get_logger().info("Node State_Publisher initialized!!!") 

    def odom_cb(self, msg):
        # POsisicón
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z

        # Orientación
        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w

        # Velocidades
        self.v = msg.twist.twist.linear.x
        self.w = msg.twist.twist.angular.z


    def timer_cb(self):
        now = self.get_clock().now().to_msg()

        # Wheel angular velocities
        wr = (self.v + (self.L / 2.0) * self.w) / self.r
        wl = (self.v - (self.L / 2.0) * self.w) / self.r

        # Integrate wheel angles
        self.right_wheel_pos += wr * self.dt
        self.left_wheel_pos += wl * self.dt

        # JointState
        self.joints.header.stamp = now
        # Pocision de las ruedas
        self.joints.position[0] = self.left_wheel_pos 
        self.joints.position[1] = self.right_wheel_pos
        # A qué velocidad gira 
        self.joints.velocity[0] = wl
        self.joints.velocity[1] = wr 

        # Publico el transform y joint
        self.joint_pub.publish(self.joints)


def main(args=None):
    rclpy.init(args=args)
    node = StatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()