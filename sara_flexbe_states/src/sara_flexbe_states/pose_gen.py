#!/usr/bin/env python
from flexbe_core import EventState, Logger
# from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point, Quaternion
from tf import transformations
import rospy


class GenPose(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose

    <= pose     Target waypoint for navigation.
    <= failed   Job as failed.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GenPose, self).__init__(outcomes=['done', 'failed'], output_keys=['pose'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        pt = Point(x=4, y=4)
        qt = transformations.quaternion_from_euler(0, 0, 0)
        userdata.pose = Pose(position=pt, orientation=Quaternion(*qt))  # One of the outcomes declared above.

        return 'done'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter Gen Pose')
