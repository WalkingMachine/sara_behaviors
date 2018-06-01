# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
import re

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
        self.test = re.compile("\$[A-z0-9]*")

    def execute(self, userdata):
        '''
        Execute this state
        '''
        text = self.ParamName
        if rospy.has_param(self.ParamName):
            userdata.Value = rospy.get_param(text)
            return "done"

        print("changing \"" + text + "\"")
        matches = self.test.findall(text)
        if matches:
            for match in matches:
                if rospy.has_param(str(match[+1:])):
                    text = text.replace(str(match), str(rospy.get_param(match[+1:])))
                    print("\t"+str(match[+1:]))
                    ok = True
                else:
                    text = text.replace(str(match), str(match[+1:]))
                    print("\t"+str(match[+1:]))
                    ok = False
            print("by \"" + text + "\"")
            userdata.Value = text
            return "done"

        return "failed"