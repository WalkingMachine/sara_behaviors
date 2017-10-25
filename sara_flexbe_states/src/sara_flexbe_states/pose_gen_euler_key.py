#!/usr/bin/env python
from flexbe_core import EventState, Logger
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose

class GenPoseEulerKey(EventState):
    '''
    ### State
    Generate a pose from xyz and euler angles keys instead of parameters

    ### input keys
    ># x
    ># y
    ># z
    ># yaw
    ># pitch
    ># roll

    ### output_keys
    #> pose generated pose

    ### outcomes
    <= done
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GenPoseEulerKey, self).__init__(outcomes=['done'], output_keys=['pose']
            ,input_keys=['x', 'y', 'z', 'yaw', 'pitch', 'roll'])
        self.pt = Pose()
        self.pt.position.x = userdata.x
        self.pt.position.y = userdata.y
        self.pt.position.z = userdata.z
        qt = quaternion_from_euler(userdata.roll, userdata.pitch, userdata.yaw)
        self.pt.orientation.w = qt[3]
        self.pt.orientation.x = qt[0]
        self.pt.orientation.y = qt[1]
        self.pt.orientation.z = qt[2]


    def execute(self, userdata):
        userdata.pose = self.pt
        return 'done'
