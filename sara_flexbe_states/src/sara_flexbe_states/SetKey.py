# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class SetKey(EventState):
    '''
    Set a Key to a predefined Value
    -- Value    object      The desired value.
    
    <# Key	    object		The key to set.
    
    <= done                 The key is set
    '''

    def __init__(self, Value):
        '''
        Constructor
        '''
        super(SetKey, self).__init__(outcomes=['done'],  output_keys=['Key'])
        self.Value = Value
    def execute(self, userdata):
        '''
        Execute this state
        '''

        userdata.Key = self.Value;
        return "done"
