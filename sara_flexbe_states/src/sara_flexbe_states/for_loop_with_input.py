#!/usr/bin/env python
from flexbe_core import EventState, Logger


class ForLoopWithInput(EventState):
    """
    Allow to loop a certain number of time. To begin with 0, the input need to be -1

    -- repeat     int      number of repetitions

    ># index_in      int       input index

    <# index_out      int     current index

    <= do        loop
    <= end       finished
    """

    def __init__(self, repeat):
        """Constructor"""

        super(ForLoopWithInput, self).__init__(outcomes=['do', 'end'], input_keys=['index_in'], output_keys=['index_out'])
        self.repeat = repeat

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if userdata.index_in < self.repeat:
            userdata.index_out = userdata.index_in + 1
            return 'do'
        else:
            userdata.index_out = 0
            return 'end'
