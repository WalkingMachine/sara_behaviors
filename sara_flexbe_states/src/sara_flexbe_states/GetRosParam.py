# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class GetRosParam(EventState):
    '''
    Get a value from the ros parameter server.
    -- ParamName    string      The desired value.
    
    #> Value      object      The rosparam to set.
    
    <= done                 The rosparam is set
    <= failed               The rosparam didn't exist
    '''

    def __init__(self, ParamName):
        '''
        Constructor
        '''
        super(GetRosParam, self).__init__(outcomes=['done', 'failed'], output_keys=['Value'])
        self.ParamName = ParamName

    def execute(self, userdata):
        '''
        Execute this state
        '''
        if rospy.has_param(self.ParamName):
            userdata.Value = rospy.get_param(self.ParamName)
            return "done"
        return "failed"
