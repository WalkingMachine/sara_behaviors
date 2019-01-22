# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 25.05.2017
@author: Philippe La Madeleine
'''


class FIFO_Add(EventState):
    '''
    Add an entry in a FIFO
    ># FIFO        object        The FIFO in which we want to add an entry.
    ># Entry       object        The value to enter.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(FIFO_Add, self).__init__(outcomes = ['done'],
                                            input_keys=['Entry','FIFO'])

    def execute(self, userdata):
        '''
        Execute this state
        '''

        return "done"

    def on_enter(self, userdata):
        userdata.FIFO.append( userdata.Entry );