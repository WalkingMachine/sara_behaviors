#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose
from sara_moveit.srv import *
import rospy


class MoveArm(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose

    ># pose     Pose2D      Target waypoint for navigation.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(MoveArm, self).__init__(outcomes=['done', 'failed'], input_keys=['pose'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        Logger.loginfo('Waiting for move_arm')
        rospy.wait_for_service('move_arm')
        Logger.loginfo('Rospy wait')

        try:
            move_arm = rospy.ServiceProxy('move_arm', move)
            if not move_arm(move_group="RightArm", pose=userdata.pose).success:
                Logger.logwarn("ERROR while calling service")
                return 'failed'
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

        Logger.loginfo('The arm should move NOW.')

        return 'done'  # One of the outcomes declared above.

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter Move Arm')
