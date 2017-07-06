# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

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
        super(FIFO_Get, self).__init__(outcomes = ['done','empty'],
                                            input_keys=['FIFO'],
                                            output_keys = ['Out'])

    def execute(self, userdata):
        '''
        Execute this state
        '''
        Count = 0
        for i in userdata.FIFO:
            Count = Count+1
        if ( Count > 0 ):
            userdata.Out = userdata.FIFO[0]
            Count = Count-1
            while Count > 0:
                userdata.FIFO[Count-1] = userdata.FIFO[Count]
                Count = Count-1
            userdata.FIFO.pop()
            return "done"
        else:
            return "empty"
