#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from std_msgs.msg import Bool

from flexbe_core.proxy import ProxyPublisher



class ContinueButton(EventState):
    '''
    Reads on a topic to see for the continue button.

    <= Continue            Continue if button pressed.
    <=

    '''

    def __init__(self):

        super(ContinueButton, self).__init__(outcomes=['Continue'])
        self.state = False


    def on_enter(self, userdata):
        Logger.loginfo('Entering continue button state')

    def execute(self, userdata):

        self.state = rospy.wait_for_message('/ui/continue', Bool, timeout=None)

        if self.state is True:
            return 'continue'



