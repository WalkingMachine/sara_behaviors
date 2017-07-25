#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
from wm_moveit_server.srv._move_joints import move_joints

import rospy


class MoveJoint(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same joint configuration

    ># joint_state     state      State Configuration.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, pose_name):
        super(MoveJoint, self).__init__(outcomes=['done', 'failed'])
        self.pose_name = pose_name

    def on_enter(self, userdata):
         Logger.loginfo('Entering move_joint service caller')

    def execute(self, userdata):
        Logger.loginfo('waiting for service /move_joints')
        try:
            rospy.wait_for_service('/move_joints', timeout=10)
        except:
            return 'failed'

        try:
            send_pose = rospy.ServiceProxy('/move_joints', move_joints)
            resp = send_pose('RightArm', self.pose_name)

            if not resp.succes:
                Logger.logwarn("ERROR while calling service")
                return 'failed'


        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

        return 'done'