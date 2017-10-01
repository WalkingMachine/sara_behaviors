#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
from tf.transformations import quaternion_from_euler


class GetMarker(EventState):
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
        super(GetMarker, self).__init__(outcomes=['done','not_found'], output_keys=['pose'])
        self.index = index
        self._topic = "/arm_pose_marker"
        self._sub = ProxySubscriberCached({self._topic: AlvarMarkers})
        self.quat = quaternion_from_euler(3.14159,0,0)

    def execute(self, userdata):
        '''
        Execute this state
        '''

        markers = userdata.pose = self._sub.get_last_msg(self._topic)
        for marker in markers.markers:
            if marker.id == self.index:
                userdata.pose = marker.pose*self.quat
                return 'done'

        return 'not_found'
