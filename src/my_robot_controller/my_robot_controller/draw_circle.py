#!usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawCircle(Node):

    def __init__(self):
        super().__init__("draw_circle")
        self.cmv_vel_pub_=self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.create_timer(.5,self.send_vel_command)
        self.get_logger().info('Draw circle node has been started')
    
    def send_vel_command(self):
        msg=Twist()
        msg.linear.x=2.0
        msg.angular.z=1.0
        self.cmv_vel_pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DrawCircle()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == '__main__':
    main()