# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class SetRosParamKey(EventState):
    '''
    Store a value in the ros parameter server for later use.
    ># ParamName    string     The desired value. Can also be a phrase with $ in it. e.g. "give me the $object"
    
    ># Value      object      The rosparam to set.
    
    <= done                 The rosparam is set
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(SetRosParamKey, self).__init__(outcomes=['done'], input_keys=['Value', 'ParamName'])

    def execute(self, userdata):
        '''
        Execute this state
        '''
        if userdata.Value:
            rospy.set_param(userdata.ParamName, userdata.Value)
        else:
            if rospy.has_param(userdata.ParamName):
                rospy.delete_param(userdata.ParamName)
        return "done"
