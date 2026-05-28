#!/usr/bin/env python3
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Float32
import transforms3d
from nav_msgs.msg import Odometry
import numpy as np
from rclpy.qos import QoSProfile, ReliabilityPolicy


class Localisation(Node): 
    def __init__(self): 
        super().__init__('puzzlebot_localization') 

        # SUBSCRIBERS
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        self.wr_sub = self.create_subscription(Float32, "/VelocityEncR", self.wr_cb, qos)
        self.wl_sub = self.create_subscription(Float32, "/VelocityEncL", self.wl_cb, qos)

        # PUBLISHERS
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # VARIABLES
        self.r = 0.05 # wheel radius
        self.L = 0.19 # wheelbase
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  

        # Wheel speeds
        self.wr = 0.0
        self.wl = 0.0

        # Speeds  
        self.v = 0.0
        self.w = 0.0

        # TIMER
        self.last_time = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.timer_callback) 
        self.get_logger().info("Node  Localisation initialized!!!") 
     

    def timer_callback(self): 
        # Velocidades
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now
        self.v = self.r * (self.wr + self.wl) / 2.0
        self.w = self.r * (self.wr - self.wl) / self.L

        # Robot pose with odometry
        self.x += self.v * np.cos(self.theta) * dt
        self.y += self.v * np.sin(self.theta) * dt
        self.theta += self.w * dt
        
        # Publish 
        odom_msg = self.odom_message(now)
        self.odom_pub.publish(odom_msg)
        self.publish_tf(odom_msg)
        
       
    def publish_tf(self, odom_msg):
        t = TransformStamped()

        t.header.stamp = odom_msg.header.stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        t.transform.rotation = odom_msg.pose.pose.orientation

        self.tf_broadcaster.sendTransform(t)

    def odom_message(self, now):
        odom_msg = Odometry()

        odom_msg.header.stamp = now.to_msg()
        odom_msg.header.frame_id = 'odom' 
        odom_msg.child_frame_id = 'base_footprint'
        odom_msg.pose.pose.position.x = self.x 
        odom_msg.pose.pose.position.y = self.y 
        odom_msg.pose.pose.position.z = 0.0

        # Quaternion
        quat = transforms3d.euler.euler2quat(0,0,self.theta) 
        odom_msg.pose.pose.orientation.w = quat[0]
        odom_msg.pose.pose.orientation.x = quat[1]
        odom_msg.pose.pose.orientation.y = quat[2]
        odom_msg.pose.pose.orientation.z = quat[3]

        # Linear and angular velocity
        odom_msg.twist.twist.linear.x = self.v
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.linear.z = 0.0

        odom_msg.twist.twist.angular.x = 0.0
        odom_msg.twist.twist.angular.y = 0.0
        odom_msg.twist.twist.angular.z = self.w

        return odom_msg
            
    def wr_cb(self, msg): 
        self.wr = msg.data

    def wl_cb(self, msg): 
        self.wl = msg.data

 

def main(args=None): 
    rclpy.init(args=args) 
    m_p=Localisation() 
    rclpy.spin(m_p) 
    m_p.destroy_node() 
    rclpy.shutdown() 

     

if __name__ == '__main__':
    main()