#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose
from sara_moveit.srv import get_pose
import rospy


class GetArmPose(EventState):
    '''
    GetArmPose return the pose of the arm

    <# pose     Pose      Target waypoint for navigation.

    <= done     Finish job.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GetArmPose, self).__init__(outcomes=['done'], output_keys=['pose'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        Logger.loginfo('Waiting for get_pose')
        rospy.wait_for_service('get_pose')
        Logger.loginfo('Rospy wait')

        try:
            get_pose = rospy.ServiceProxy('get_pose', get_pose)
            resp = get_pose(move_group="RightArm", pose=userdata.pose)
            Logger.loginfo('service called')
            userdata.pose = resp.pose
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)


        return 'done'  # One of the outcomes declared above.

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter get arm pose')
