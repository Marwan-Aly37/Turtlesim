#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import subprocess
import random
import time
#second turtle coordinates
x2 = random.uniform(1,10)
y2 = random.uniform(1,10)
#third turtle coordinates
x3 = random.uniform(1,10)
y3 = random.uniform(1,10)
#fourth turtle coordinates
x4 = random.uniform(1,10)
y4 = random.uniform(1,10)

def launch_turtlesim(): 
    subprocess.Popen(['ros2','run','turtlesim','turtlesim_node'])
    subprocess.Popen(['ros2','run','turtlesim','turtle_teleop_key'])

def spawn(x,y,name):
    service_call_command = f"ros2 service call /spawn turtlesim/srv/Spawn '{{x: {x}, y: {y}, theta: {0.0}, name: \"{name}\"}}'"
    subprocess.run(service_call_command, shell=True)

launch_turtlesim()
time.sleep(2)
spawn(x2,y2,"turtle2")
spawn(x3,y3,"turtle3")
spawn(x4,y4,"turtle4")

class Position(Node):
    def __init__(self):
        super().__init__('position_node')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.sub_callback,
            10
        )
        

    def sub_callback(self, msg):
        global x2,y2,x3,y3,x4,y4
        def kill(name):
            kill_command = f"ros2 service call /kill turtlesim/srv/Kill '{{name: \"{name}\"}}'"            
            subprocess.run(kill_command,shell = True)  
        #check on turtle2
        if (abs(msg.x-x2) <= 0.5) and (abs(msg.y-y2) <= 0.5):
            kill("turtle2")
            x2 = random.uniform(1,10)
            y2 = random.uniform(1,10)
            spawn(x2,y2,"turtle2")
        #check on turtle3
        if (abs(msg.x-x3) <= 0.5) and (abs(msg.y-y3) <= 0.5):
            kill("turtle3")
            x3 = random.uniform(1,10)
            y3 = random.uniform(1,10)
            spawn(x3,y3,"turtle3")
        #check on turtle4
        if (abs(msg.x-x4) <= 0.5) and (abs(msg.y-y4) <= 0.5):
            kill("turtle4")
            x4 = random.uniform(1,10)
            y4 = random.uniform(1,10)
            spawn(x4,y4,"turtle4")


def main(args=None):
    rclpy.init(args=args)
    position_node = Position()
    rclpy.spin(position_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
