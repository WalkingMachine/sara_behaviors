# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
from rospy.exceptions import ROSInterruptException

'''
Created on 11.06.2013
@author: Philipp Schillinger
'''


class FIFOAddState(EventState):
    '''
    Add an entry in a FIFO
    ># FIFO	    object		The FIFO in which we want to add an entry.
    ># Entry	object		The value to enter.
    <# FIFO     object      The new FIFO
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(DecisionState, self).__init__(outcomes = ['done'],
                                            input_keys=['Entry','FIFO'],
                                            output_keys = ['FIFO_Out'])

    def execute(self, userdata):
        '''
        Execute this state
        '''

        return "done"

    def on_enter(self, userdata):
        userdata.FIFO.append( userdata.Entry );
        userdata.FIFO_Out = userdata.FIFO;