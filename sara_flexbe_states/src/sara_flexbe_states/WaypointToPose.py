#!/usr/bin/env python

from flexbe_core import EventState, Logger
from tf import transformations
from geometry_msgs.msg import Pose, Point, Quaternion


class WpToPose(EventState):
    '''
    Transforms Waypoint to pose


    ># data uint8		uint8 to publish.
    ># topic    string       topic to publish on.
    <= done            state of the process
    <= failed            state of the process.

    '''

    def __init__(self):

        super(WpToPose, self).__init__(input_keys=['waypoint_id'],
                                          outcomes=['done', 'failed'], output_keys=['pose'])


    def on_enter(self, userdata):
	    Logger.loginfo('Entering waypoint to pose transformation')

    def execute(self, userdata):

		
	    return 'done'

