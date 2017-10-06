#!/usr/bin/env python
from flexbe_core import EventState, Logger
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose

class GenPoseEuler(EventState):
    '''
    Generate a pose from xyz and euler angles
    x       x
    y       y
    z       z
    roll    roll
    pitch    pitch
    yaw      yaw

    <= pose   generated pose
    '''

    def __init__(self, x, y, z, roll, pitch, yaw):
        # See example_state.py for basic explanations.
        super(GenPoseEuler, self).__init__(outcomes=['done'], output_keys=['pose'])
        self.pt = Pose()
        self.pt.position.x = x
        self.pt.position.y = y
        self.pt.position.z = z
        qt = quaternion_from_euler(roll, pitch, yaw)
        self.pt.orientation.w = qt[0]
        self.pt.orientation.x = qt[1]
        self.pt.orientation.y = qt[2]
        self.pt.orientation.z = qt[3]


    def execute(self, userdata):
        userdata.pose = self.pt
        return 'done'