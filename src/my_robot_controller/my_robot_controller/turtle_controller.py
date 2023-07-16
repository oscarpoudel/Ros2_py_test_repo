#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')
        self.get_logger().info('Turtle controller node started')
        self.publr = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.subcr= self.create_subscription(Pose,'/turtle1/pose',self.callback_fun,10)
        self.previous_x = 0.0
    
    def callback_fun(self,pose:Pose):
        cmd = Twist()
        if pose.x > 9 or pose.x <2 or pose.y < 2 or pose.y > 9:
            cmd.linear.x=2.0
            cmd.angular.z=1.5
        else:
            cmd.linear.x = 1.0
        self.publr.publish(cmd)

        if pose.x > 5.5 and self.previous_x <=5.5 :
            self.previous_x = pose.x
            self.call_set_pen(255,0,0,3,0)
        elif pose.x <= 5.5 and self.previous_x > 5.5:
            self.previous_x = pose.x
            self.call_set_pen(0,255,0,3,0)
    
    def call_set_pen(self,r,g,b,width,off):
        client = self.create_client(SetPen,"/turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger().warn('Waiting for the service...')
        
        request=SetPen.Request()
        request.r=r
        request.g=g
        request.b=b
        request.width=width
        request.off = off

        future=client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))
    
    def callback_set_pen(self,future):
        try:
            response=future.results()
        except Exception as e:
            self.get_logger().error("Service call failed: %r"%(e))


def main(args=None):

    rclpy.init(args=args)
    node = TurtleController()

    rclpy.spin(node)
    rclpy.shutdown()


# if __name__ == '__main__':
#     main()