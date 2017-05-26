# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
from collections import deque

'''
Created on 25.05.2017
@author: Philippe La Madeleine
'''


class FIFO_Get(EventState):
    '''
    Take away the last entry from a FIFO
    ># FIFO	    object		The FIFO in which we want to add an entry.
    <# Out	object		The value on top of the FIFO.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(FIFO_Get, self).__init__(outcomes = ['done'],
                                            input_keys=['FIFO'],
                                            output_keys = ['Out'])

    def execute(self, userdata):
        '''
        Execute this state
        '''

        return "done"

    def on_enter(self, userdata):
        userdata.Out = userdata.FIFO.popleft();

