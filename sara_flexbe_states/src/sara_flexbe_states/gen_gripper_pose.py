#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, Quaternion
from tf.transformations import quaternion_from_euler

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- offset_x    float      offset x
    -- offset_y    float      offset y
    -- offset_z    float      offset z
    -- offset_tetha  float      offset theta around the Z axis
    
    >= pose_in     Pose     input pose
    <= pose_out    Pose     output pose
    '''

    def __init__(self, x, y, z, t):
        super(GenGripperPose, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.x = x
        self.y = y
        self.z = z
        quat = quaternion_from_euler(0, 0, t)
        self.quat = Quaternion()
        self.quat.x = -0.460612186114*quat[0]
        self.quat.y = -0.46897814506*quat[1]
        self.quat.z = 0.501742587173*quat[2]
        self.quat.w = 0.56227243368*quat[3]

    def execute(self, userdata):

        out = Pose()
        out.position.x = userdata.pose_in.position.x-0.20+self.x
        out.position.y = userdata.pose_in.position.y+self.y
        out.position.z = userdata.pose_in.position.z+0.05+self.z
        out.orientation = self.quat

        userdata.pose_out = out
        return 'done'
