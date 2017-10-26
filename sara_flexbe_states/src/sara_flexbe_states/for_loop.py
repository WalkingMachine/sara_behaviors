#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy


class ForLoop(EventState):
    """
    Allow to loop a certain number of time

    -- repeat     int      number of repetitions

    
    <= index     current index

    <= do        loop
    <= end       finished       
    """

    def __init__(self, repeat):
        """Constructor"""

        super(ForLoop, self).__init__(outcomes = ['do','end'], output_keys = ['index'])
        self.repeat = repeat
        self.index = 1

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if ( self.index <= self.repeat ):
            self.index = self.index+1
            userdata.index = self.index
            return 'do'
        else:
            self.index = 1
            return 'end'

