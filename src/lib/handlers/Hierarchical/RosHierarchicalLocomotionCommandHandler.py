#!/usr/bin/env python
import rospy, math, subprocess, os, sys
import logging
import globalConfig

from geometry_msgs.msg import Twist
"""
==================================================================
rosLocomotionCommand.py - ros Locomotion Command Handler
==================================================================
"""

import lib.handlers.handlerTemplates as handlerTemplates


class RosHierarchicalLocomotionCommandHandler(
        handlerTemplates.LocomotionCommandHandler):
    def __init__(self,
                 executor,
                 shared_data,
                 velocityTopic='/cmd_vel_mux/input/navi'):
        """
        The ROS Locomotion Command Handler

        velocityTopic (str): This is the topic which handles the movement commands (default='/cmd_vel_mux/input/navi')
        """

        try:
            rospy.init_node('RosLocoHandler', anonymous=True, disable_signals=True)
            #open a publisher for the base controller of the robot
            # TODO: queue size okay?
        except Exception as e:
            logging.warning('Rospy node already initialized')

        self.pub = rospy.Publisher(velocityTopic, Twist, queue_size=10)
        # for the pr2, use /base_controller/command
        # the turtlebot takes /cmd_vel

    def sendCommand(self, cmd):
        #Twist is the message type and consists of x,y,z linear velocities
        #and roll, pitch, yaw orientation velocities (x,y,z)
        twist = Twist()
        #Positive x is forward on robots in Gazebo
        twist.linear.x = cmd[0] * 4
        if twist.linear.x < 0:
            twist.linear.x = 0

        #Positive z is upward on robots in Gazebo
        twist.linear.z = cmd[2] * 4
        if twist.linear.z < 0:
            twist.linear.z = 0

        #Angluar z is yaw or rotation in the xy plane
        twist.angular.z = cmd[1] * 1.5
        try:
            #Publish the command to the robot
            self.pub.publish(twist)
        except Exception as e :
            print 'Error publishing Twist Command', e