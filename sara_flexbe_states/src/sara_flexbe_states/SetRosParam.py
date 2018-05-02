# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class SetRosParam(EventState):
    '''
    Store a value in the ros parameter server for later use.
    -- ParamName    string      The desired value.
    
    ># Value      object      The rosparam to set.
    
    <= done                 The rosparam is set
    '''

    def __init__(self, ParamName):
        '''
        Constructor
        '''
        super(SetRosParam, self).__init__(outcomes=['done'], input_keys=['Value'])
        self.ParamName = ParamName

    def execute(self, userdata):
        '''
        Execute this state
        '''
        if userdata.Value:
            rospy.set_param(self.ParamName, userdata.Value)
        else:
            if rospy.has_param(self.ParamName):
                rospy.delete_param(self.ParamName)
        return "done"
