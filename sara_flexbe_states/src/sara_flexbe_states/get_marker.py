#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker

class Get_Robot_Pose(EventState):
    '''
    Gets the pose of a AR marker.
    
    -- index  index of the marker.
    -- 

    #> pose         geometry_msgs.Pose        Current pose of the AR marker.

    <= done         The pose is received.
    <= not_found         The marker is not found

    '''

    def __init__(self, index):
        '''
        Constructor
        '''
        super(Get_Robot_Pose, self).__init__(outcomes=['done'], output_keys=['pose'])
        self.index = index
        self._topic = "/arm_pose_marker"
        self._sub = ProxySubscriberCached({self._topic: AlvarMarkers})

    def execute(self, userdata):
        '''
        Execute this state
        '''

        markers = userdata.pose = self._sub.get_last_msg(self._topic)
        for marker in markers.markers:
            if marker.id == self.index:
                userdata.pose = marker.pose
                break

        return 'done'
