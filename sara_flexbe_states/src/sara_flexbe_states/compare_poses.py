#!/usr/bin/env python
from flexbe_core import EventState, Logger
# from std_msgs.msg import String
from geometry_msgs.msg import Pose
import rospy
import math

class AmclInit(EventState):
    '''
    get a pose between two poses


    <= pose     Target waypoint for navigation.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(AmclInit, self).__init__(outcomes=['done'], input_keys=['pose_robot', 'pose_other'], output_keys=['pose'])


    def execute(self, userdata):


        userdata.pose = Pose()
        dx = userdata.pose_robot.position.x+userdata.pose_other.position.x
        dy = userdata.pose_robot.position.y+userdata.pose_other.position.y
        dz = userdata.pose_robot.position.z+userdata.pose_other.position.z
        dist = math.sqrt( dx*dx+dy*dy+dz*dz )
        if dist > 1.5:
            userdata.pose.position.x = userdata.pose_robot.position.x+dx/dist
            userdata.pose.position.y = userdata.pose_robot.position.y+dy/dist
            userdata.pose.position.z = userdata.pose_robot.position.z+dz/dist
            userdata.pose.orientation = userdata.pose_other.orientation
        else:
            userdata.pose = userdata.pose_robot;

        return 'done'
