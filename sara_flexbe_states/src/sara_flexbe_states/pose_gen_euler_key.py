#!/usr/bin/env python
from flexbe_core import EventState, Logger
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose

class GenPoseEulerKey(EventState):
    '''
    ### State
    Generate a pose from xyz and euler angles keys instead of parameters

    ># x        double      the x coordinate
    ># y        double      the x coordinate
    ># z        double      the x coordinate
    ># yaw      double      the yaw angle
    ># pitch    double      the pitch angle
    ># roll     double      the roll angle

    #> pose     geometry_msgs/Pose        the generated pose

    <= done     The generation is succesfull
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GenPoseEulerKey, self).__init__(outcomes=['done'], output_keys=['pose'],input_keys=['xpos', 'ypos', 'zpos', 'yaw', 'pitch', 'roll'])
        self.pt = Pose()

    def execute(self, userdata):
        print("HLLEO")
        self.pt.position.y = userdata.ypos
        self.pt.position.z = userdata.zpos
        self.pt.position.x = userdata.xpos
        qt = quaternion_from_euler(userdata.roll, userdata.pitch, userdata.yaw)
        self.pt.orientation.w = qt[3]
        self.pt.orientation.x = qt[0]
        self.pt.orientation.y = qt[1]
        self.pt.orientation.z = qt[2]

        userdata.pose = self.pt
        return 'done'
