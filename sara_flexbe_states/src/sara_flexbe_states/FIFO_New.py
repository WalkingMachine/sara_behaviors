# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
from collections import deque

'''
Created on 25.05.2017
@author: Philippe La Madeleine
'''


class FIFO_New(EventState):
    '''
    Clear a FIFO
    <# FIFO     object      The new FIFO
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(FIFO_New, self).__init__(outcomes = ['done'],
                                            output_keys = ['FIFO'])

    def execute(self, userdata):
        '''
        Execute this state
        '''

        return "done"

    def on_enter(self, userdata):
        userdata.FIFO = deque();