#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger



class StringListLogger(EventState):
    '''
    MoveArm receive a ROS pose as input and launch a ROS service with the same pose

    ># List     string[]      list to log

    <= done     Finish job.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(StringListLogger, self).__init__(outcomes=['done'], input_keys=['List'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.

        return 'done'  # One of the outcomes declared above.

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.
        if userdata.List != None:
            for line in userdata.List:
                Logger.loginfo(line)
