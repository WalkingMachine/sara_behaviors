#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from geometry_msgs.msg import Pose, PoseStamped


class Get_Robot_Pose(EventState):
    '''
    Gets the current pose of the robot.

    #> pose         geometry_msgs.Pose        Current pose of the robot.

    <= done         The pose is received.

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Get_Robot_Pose, self).__init__(outcomes=['done'], output_keys=['pose'])

        self._topic = "/robot_pose"
        self._sub = ProxySubscriberCached({self._topic: Pose})

    def execute(self, userdata):
        '''
        Execute this state
        '''

        mypose = userdata.pose = self._sub.get_last_msg(self._topic)
        if mypose:
            Logger.loginfo('my pose is:'+str(mypose))
            userdata.pose = mypose
        else:
            userdata.pose = Pose()
        return 'done'
