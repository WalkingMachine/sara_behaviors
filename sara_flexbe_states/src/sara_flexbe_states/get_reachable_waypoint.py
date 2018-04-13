#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Pose, Point
import math


class Get_Reacheable_Waypoint(EventState):
    '''
    Get a position close enough to reach a point without stepping on it

    -- Distance     float                           decalage distance to point

    #> pose_in      geometry_msgs.Pose/Point        Position to reach
    #< pose_out     geometry_msgs.Pose              Output position

    <= done         position found

    '''

    def __init__(self, Distance):
        '''
        Constructor
        '''
        super(Get_Reacheable_Waypoint, self).__init__(outcomes=['done'], input_keys=['pose_in'], output_keys=['pose_out'])

        self._topic = "/robot_pose"
        self._sub = ProxySubscriberCached({self._topic: Pose})
        self.Distance = Distance

    def execute(self, userdata):
        '''
        Execute this state
        '''

        mypose = userdata.pose = self._sub.get_last_msg(self._topic)
        Logger.loginfo('my pose is:'+str(mypose))

        Out = Pose()
        targetPose = Pose()

        if type(userdata.pose_in) is Pose:
            Logger.loginfo('the target is a pose')
            targetPose = userdata.pose_in

        elif type(userdata.pose_in) is Point:
            Logger.loginfo('the target is a point')
            targetPose.position = userdata.pose_in

        length = ((targetPose.position.x-mypose.position.x)**2 + (targetPose.position.y-mypose.position.y)**2 )**0.5
        Out.position.x = targetPose.position.x - (targetPose.position.x-mypose.position.x)/length*self.Distance
        Out.position.y = targetPose.position.y - (targetPose.position.y-mypose.position.y)/length*self.Distance

        angle = math.atan2((targetPose.position.y - mypose.position.y), (targetPose.position.x - mypose.position.x))
        qt = quaternion_from_euler(0, 0, angle)
        Out.orientation.w = qt[3]
        Out.orientation.x = qt[0]
        Out.orientation.y = qt[1]
        Out.orientation.z = qt[2]

        userdata.pose_out = Out

        return 'done'
