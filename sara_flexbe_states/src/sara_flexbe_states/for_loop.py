#!/usr/bin/env python
from flexbe_core import EventState, Logger


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

        super(ForLoop, self).__init__(outcomes=['do', 'end'], output_keys=['index'])
        self.repeat = repeat
        self.index = 0

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        userdata.index = self.index

        if self.index < self.repeat:
            self.index += 1
            return 'do'
        else:
            self.index = 0
            return 'end'
