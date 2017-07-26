#!/usr/bin/env python
from flexbe_core import EventState, Logger
# from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovariance
import rospy


class AmclInit(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose
    (x,y,z)
    (x,y,z,w)

    <= pose     Target waypoint for navigation.
    <= failed   Job as failed.
    '''

    def __init__(self, x, y, z, ox, oy, oz, ow):
        # See example_state.py for basic explanations.
        super(AmclInit, self).__init__(outcomes=['done', 'failed'], output_keys=['pose'])

        self._x = 0
        if x is not None: self._x = x

        self._y = 0
        if y is not None: self._y = y

        self._z = 0
        if z is not None: self._z = z

        self._ox = 0
        if x is not None: self._ox = ox

        self._oy = 0
        if y is not None: self._oy = oy

        self._oz = 0
        if z is not None: self._oz = oz

        self._ow = 0
        if w is not None: self._ow = ow



    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        pt = PoseWithCovariance()
        pt.covariance = [0.001, 0, 0, 0, 0, 0,
                         0, 0.001, 0, 0, 0, 0,
                         0, 0, 100000, 0, 0, 0,
                         0, 0, 0, 100000, 0, 0,
                         0, 0, 0, 0, 100000, 0,
                         0, 0, 0, 0, 0, 1000]

        pt.pose.position.x = self._x
        pt.pose.position.y = self._y
        pt.pose.position.z = self._z

        pt.pose.position.ox = self._ox
        pt.pose.position.oy = self._oy
        pt.pose.position.oz = self._oz
        pt.pose.position.ow = self._ow

        userdata.pose = pt

        return 'done'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter Gen Pose')
