#!/usr/bin/env python
from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose

class GenPoseQuat(EventState):
    '''
    Generate a pose from xyz and quaternion

    ># x        double      the x coordinate
    ># y        double      the x coordinate
    ># z        double      the x coordinate
    ># ox       double      the ox coordinate
    ># oy       double      the oy coordinate
    ># oz       double      the oz coordinate
    ># ow       double      the ow coordinate

    #> pose     geometry_msgs/Pose        the generated pose

    <= done     The generation is succesfull
    '''

    def __init__(self, x, y, z, ox, oy, oz, ow):
        super(GenPoseQuat, self).__init__(outcomes=['done'], output_keys=['pose'])

        self.pt = Pose()
        self.pt.position.x = x
        self.pt.position.y = y
        self.pt.position.z = z
        self.pt.orientation.x = ox
        self.pt.orientation.y = oy
        self.pt.orientation.z = oz
        self.pt.orientation.w = ow

    def execute(self, userdata):
        userdata.pose = self.pt
        return 'done'
