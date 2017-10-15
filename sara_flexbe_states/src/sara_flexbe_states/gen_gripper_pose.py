#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- offset_x    int      offset
    -- offset_y    int      offset
    -- offset_z    int      offset
    
    >= pose_in     Pose     input pose
    <= pose_out    Pose     output pose
    '''

    def __init__(self, x, y, z):
        super(GenGripperPose, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.x = x
        self.y = y
        self.z = z


    def execute(self, userdata):

        out = Pose()
        out.position.x = userdata.pose_in.position.x-0.20+self.x
        out.position.y = userdata.pose_in.position.y+self.y
        out.position.z = userdata.pose_in.position.z+0.05+self.z
        out.orientation.x = -0.460612186114
        out.orientation.y = -0.46897814506
        out.orientation.z = 0.501742587173
        out.orientation.w = 0.56227243368
        userdata.pose_out = out
        return 'done'
