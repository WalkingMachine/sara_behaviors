#!/usr/bin/env python
from __future__ import print_function
from flexbe_core import EventState, Logger
import std_srvs
import rospy
from std_srvs.srv._SetBool import SetBool
#from std_msgs.msg.Bool import Bool

class StartFace(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self):
        super(StartFace, self).__init__(outcomes=['done', 'failed'])

    def on_enter(self, userdata):
         Logger.loginfo('Setting emotion and brightness')

    def execute(self, userdata):
        Logger.loginfo('Waiting for service sara_face/Start ')

        try:
            rospy.wait_for_service('sara_face/Start', timeout=10)
        except:
            return 'failed'

        try:
            set_expression = rospy.ServiceProxy('sara_face/Start', SetBool)
            resp = set_expression(True)
            Logger.loginfo('service called')

            if not resp.success:
                Logger.logwarn("ERROR while calling service")
                return 'failed'
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

        Logger.loginfo('The face is ready now!')

        return 'done'

