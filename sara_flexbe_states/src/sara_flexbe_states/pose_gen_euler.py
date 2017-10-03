#!/usr/bin/env python
from flexbe_core import EventState, Logger
# from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point, Quaternion
from tf import transformations
import rospy


class GenPoseEuler(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose
    (x,y,z)
    roll =  quaternion_from_euler(0, X, X)
    pitch = quaternion_from_euler(X, 0, X)
    yaw =   quaternion_from_euler(X, X, 0)

    <= pose     Target waypoint for navigation.
    <= failed   Job as failed.
    '''

    def __init__(self, x, y, z, roll, pitch, yaw):
        # See example_state.py for basic explanations.
        super(GenPoseEuler, self).__init__(outcomes=['done', 'failed'], output_keys=['pose'])

        self._x = 0
        if x is not None: self._x = x

        self._y = 0
        if y is not None: self._y = y

        self._z = 0
        if z is not None: self._z = z

        self._roll = 0
        if roll is not None: self._roll = roll

        self._pitch = 0
        if pitch is not None: self._pitch = pitch

        self._yaw = 0
        if yaw is not None: self._yaw = yaw

        print("(", x, ",", y, ",", z, ") - (", roll, ",", pitch, ",", yaw)


    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        pt = Point(self._x, self._y, self._z)
        qt = transformations.quaternion_from_euler(self._roll, self._pitch, self._yaw)
        userdata.pose = Pose(position=pt, orientation=Quaternion(*qt))  # One of the outcomes declared above.

        return 'done'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        Logger.loginfo('Enter Gen Pose')
