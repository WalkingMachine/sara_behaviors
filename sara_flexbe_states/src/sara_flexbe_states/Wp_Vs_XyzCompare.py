#!/usr/bin/env python

from flexbe_core import EventState, Logger
from tf import transformations
from geometry_msgs.msg import Pose, Point, Quaternion


class TestCompare(EventState):
    '''
    Compares waypoint and xyz and creates pose


    ># data     uint8        uint8 to publish.
    ># topic    string       topic to publish on.
    <= done     uint8 has been published.

    '''

    def __init__(self):

        super(TestCompare, self).__init__(input_keys=['x','y', 'z','theta','waypoint_id'],
                                          outcomes=['done', 'waypoint', 'failed'], output_keys=['wp'])


    def on_enter(self, userdata):
        Logger.loginfo('Processing waypoint of the entity')

    def execute(self, userdata):


        if userdata.waypoint_id is not None:
            userdata.wp = userdata.waypoint_id
            return 'waypoint'

        if userdata.x is None:
            Logger.loginfo('There is no X')
            return 'failed'

        if userdata.y is None:
            Logger.loginfo('There is no Y')
            return 'failed'

        if userdata.z is None:
            Logger.loginfo('There is no Z')
            return 'failed'

        if userdata.theta is None:
            Logger.loginfo('There is no Theta')
            return 'failed'

        pt = Point(userdata.x, userdata.y, userdata.z)
        qt = transformations.quaternion_from_euler(0, 0, userdata.theta)
        userdata.pose = Pose(position=pt, orientation=Quaternion(*qt))

        return 'done'

