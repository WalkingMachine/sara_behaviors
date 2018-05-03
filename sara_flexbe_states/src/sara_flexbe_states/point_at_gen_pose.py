#!/usr/bin/env python

from flexbe_core import EventState
import rospy
import math
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler

class point_at_gen_pose(EventState):
    """
        calculates a pose from xyz for the gripper to point at something

    -- offsetx        double      the x coordinate
    -- offsety        double      the y coordinate
    -- offsetz        double      the z coordinate
    -- l              double      arm's length

    ># yaw      double      the yaw angle
    ># pitch    double      the pitch angle

    #> pose     geometry_msgs/Pose        the generated pose

    <= done               when calculation is over
    """

    def __init__(self, offsetx, offsety, offsetz, l):
        """Constructor"""

        super(point_at_gen_pose, self).__init__(input_keys=['yaw', 'pitch'], outcomes=['pose'], output_keys=['pose'])

        self.offsety = offsety
        self.offsetx = offsetx
        self.offsetz = offsetz
        self.l = l

    def execute(self, userdata):
        pose = Pose()
        pose.position.y = math.sin(userdata.yaw) * self.l * math.cos(userdata.pitch) + self.offsety
        pose.position.x = math.cos(userdata.yaw) * self.l * math.cos(userdata.pitch) + self.offsetx
        pose.position.z = -math.sin(userdata.pitch)*self.l + self.offsetz

        qt = quaternion_from_euler(0, userdata.pitch, userdata.yaw)
        pose.orientation.x = qt[0]
        pose.orientation.y = qt[1]
        pose.orientation.z = qt[2]
        pose.orientation.w = qt[3]

        userdata.pose=pose

        return "pose"
