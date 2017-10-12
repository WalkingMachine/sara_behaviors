#!/usr/bin/env python
from flexbe_core import EventState, Logger

class GenGripperPose(EventState):
    '''
    Apply a transformation to a pose to get a gripper friendly pose
    -- offset_x    int     offset
    -- offset_y    int     offset
    -- offset_z    int     offset
    
    >= pose_in    input pose
    <= pose_out   output pose
    '''

    def __init__(self, x, y, z):
        super(GenGripperPose, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self.x = x
        self.y = y
        self.z = z


    def execute(self, userdata):

        userdata.pose_out.position.x = userdata.pose_in.position.x-0.20+self.x
        userdata.pose_out.position.y = userdata.pose_in.position.y+self.y
        userdata.pose_out.position.z = userdata.pose_in.position.z+0.05+self.z
        userdata.pose_out.orientation.x = -0.460612186114
        userdata.pose_out.orientation.y = -0.46897814506
        userdata.pose_out.orientation.z = 0.501742587173
        userdata.pose_out.orientation.w = 0.56227243368

        return 'done'
