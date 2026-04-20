import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import transforms3d
import numpy as np
import math

class FramePublisher(Node):

    def __init__(self):
        super().__init__('puzzlebot_transforms')
        
        # Broadcasters initialization
        self.map_broadcaster = StaticTransformBroadcaster(self)
        self.base_link_broadcaster = StaticTransformBroadcaster(self)
        self.caster_link_broadcaster = StaticTransformBroadcaster(self)
        self.odom_broadcaster = TransformBroadcaster(self)

        # Static TF: world -> map
        tf_msg_map = TransformStamped()
        tf_msg_map.header.stamp = self.get_clock().now().to_msg()
        tf_msg_map.header.frame_id = 'world'
        tf_msg_map.child_frame_id = 'map'
        tf_msg_map.transform.translation.x = 0.0
        tf_msg_map.transform.translation.y = 0.0
        tf_msg_map.transform.translation.z = 0.0
        q = transforms3d.euler.euler2quat(0, 0, 0)
        tf_msg_map.transform.rotation.x, tf_msg_map.transform.rotation.y, \
        tf_msg_map.transform.rotation.z, tf_msg_map.transform.rotation.w = q[1], q[2], q[3], q[0]

        # Static TF: base_footprint -> base_link
        tf_msg_base_link = TransformStamped()
        tf_msg_base_link.header.stamp = self.get_clock().now().to_msg()
        tf_msg_base_link.header.frame_id = 'base_footprint'
        tf_msg_base_link.child_frame_id = 'base_link'
        tf_msg_base_link.transform.translation.z = 0.05
        q = transforms3d.euler.euler2quat(0, 0, 0)
        tf_msg_base_link.transform.rotation.x, tf_msg_base_link.transform.rotation.y, \
        tf_msg_base_link.transform.rotation.z, tf_msg_base_link.transform.rotation.w = q[1], q[2], q[3], q[0]

        # Static TF: base_link -> caster_link
        tf_msg_caster = TransformStamped()
        tf_msg_caster.header.stamp = self.get_clock().now().to_msg()
        tf_msg_caster.header.frame_id = 'base_link'
        tf_msg_caster.child_frame_id = 'caster_link'
        tf_msg_caster.transform.translation.x = -0.09
        tf_msg_caster.transform.translation.z = -0.043
        q = transforms3d.euler.euler2quat(0, 0, 0)
        tf_msg_caster.transform.rotation.x, tf_msg_caster.transform.rotation.y, \
        tf_msg_caster.transform.rotation.z, tf_msg_caster.transform.rotation.w = q[1], q[2], q[3], q[0]

        # Broadcast static frames
        self.map_broadcaster.sendTransform([tf_msg_map])
        self.base_link_broadcaster.sendTransform([tf_msg_base_link])
        self.caster_link_broadcaster.sendTransform([tf_msg_caster])

        # Dynamic TF structures
        self.odom_transform = TransformStamped()
        self.base_footprint_transform = TransformStamped()
        self.wheel_r_link_transform = TransformStamped()
        self.wheel_l_link_transform = TransformStamped()
        
        # Dynamic broadcasters
        self.tf_odom = TransformBroadcaster(self)
        self.tf_base_footprint = TransformBroadcaster(self)
        self.tf_wheel_r = TransformBroadcaster(self)
        self.tf_wheel_l = TransformBroadcaster(self)

        # Motion parameters (20 Hz)
        self.timer = self.create_timer(0.05, self.timer_cb)
        self.start_time = self.get_clock().now()
        self.radius = 1.5 
        self.angular_speed = 0.5 

    def timer_cb(self):
        """Update dynamic transforms."""
        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        angle = elapsed_time * self.angular_speed

        # Map -> Odom (Circular motion)
        self.odom_transform.header.stamp = self.get_clock().now().to_msg()
        self.odom_transform.header.frame_id = 'map'
        self.odom_transform.child_frame_id = 'odom'
        self.odom_transform.transform.translation.x = self.radius * np.cos(angle)
        self.odom_transform.transform.translation.y = self.radius * np.sin(angle)
        q_yaw = transforms3d.euler.euler2quat(0, 0, angle + np.pi/2)
        self.odom_transform.transform.rotation.x, self.odom_transform.transform.rotation.y, \
        self.odom_transform.transform.rotation.z, self.odom_transform.transform.rotation.w = q_yaw[1], q_yaw[2], q_yaw[3], q_yaw[0]

        # Odom -> Base Footprint
        self.base_footprint_transform.header.stamp = self.get_clock().now().to_msg()
        self.base_footprint_transform.header.frame_id = 'odom'
        self.base_footprint_transform.child_frame_id = 'base_footprint'
        q = transforms3d.euler.euler2quat(0, 0, 0)
        self.base_footprint_transform.transform.rotation.x, self.base_footprint_transform.transform.rotation.y, \
        self.base_footprint_transform.transform.rotation.z, self.base_footprint_transform.transform.rotation.w = q[1], q[2], q[3], q[0]

        # Wheels rotation (Base Link -> Wheels)
        for tf, y_offset in [(self.wheel_r_link_transform, -0.095), (self.wheel_l_link_transform, 0.095)]:
            tf.header.stamp = self.get_clock().now().to_msg()
            tf.header.frame_id = 'base_link'
            tf.child_frame_id = 'wheel_r_link' if y_offset < 0 else 'wheel_l_link'
            tf.transform.translation.x = 0.052
            tf.transform.translation.y = y_offset
            tf.transform.translation.z = -0.0025
            q_w = transforms3d.euler.euler2quat(0, angle * 3, 0)
            tf.transform.rotation.x, tf.transform.rotation.y, \
            tf.transform.rotation.z, tf.transform.rotation.w = q_w[1], q_w[2], q_w[3], q_w[0]

        # Publish all dynamic frames
        self.tf_odom.sendTransform(self.odom_transform)
        self.tf_base_footprint.sendTransform(self.base_footprint_transform)
        self.tf_wheel_r.sendTransform(self.wheel_r_link_transform)
        self.tf_wheel_l.sendTransform(self.wheel_l_link_transform)

def main(args=None):
    rclpy.init(args=args)
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        node.destroy_node()

if __name__ == '__main__':
    main()