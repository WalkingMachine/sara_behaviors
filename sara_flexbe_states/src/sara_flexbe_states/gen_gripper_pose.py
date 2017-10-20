#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler, quaternion_multiply

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- offset_x    float      offset x
    -- offset_y    float      offset y
    -- offset_z    float      offset z
    -- offset_tetha  float      offset theta around the Z axis

    >= pose_in     Pose/point     input pose
    <= pose_out    Pose     output pose
    '''

    def __init__(self, x, y, z, t):
        super(GenGripperPose, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.x = x
        self.y = y
        self.z = z
        quat1 = quaternion_from_euler(0, 0, t)
        quat2 = [-0.460612186114,
                 -0.46897814506,
                 0.501742587173,
                 0.56227243368]
        quat = quaternion_multiply(quat1, quat2)

        self.quat = Quaternion()
        self.quat.x = quat[0]
        self.quat.y = quat[1]
        self.quat.z = quat[2]
        self.quat.w = quat[3]


    def execute(self, userdata):

        out = Pose()
        if type(userdata.pose_in) is Pose:
            out.position.x = userdata.pose_in.position.x-0.20+self.x
            out.position.y = userdata.pose_in.position.y+self.y
            out.position.z = userdata.pose_in.position.z+0.05+self.z
        elif type(userdata.pose_in) is Point:
            out.position.x = userdata.pose_in.x-0.20+self.x
            out.position.y = userdata.pose_in.y+self.y
            out.position.z = userdata.pose_in.z+0.05+self.z
        else:

            Logger.loginfo('ERROR in '+str(self.name)+' : pose_in is not a Pose() nor a Point()')
            return 'done'

        out.orientation = self.quat
        userdata.pose_out = out
        return 'done'
