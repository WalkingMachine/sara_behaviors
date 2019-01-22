# !/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
import re

'''
Created on 21.09.2017
@author: Philippe La Madeleine
'''


class GetRosParamKey(EventState):
    '''
    Get a value from the ros parameter server.
    ># ParamName    string      The desired value. Can also be a phrase with $ in it. e.g. "give me the $object"
    
    #> Value      object      The rosparam to set.
    
    <= done                 The rosparam is set
    <= failed               The rosparam didn't exist
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(GetRosParamKey, self).__init__(outcomes=['done', 'failed'], input_keys=['ParamName'], output_keys=['Value'])
        self.test = re.compile("\$[A-z0-9/\-_]*")

    def execute(self, userdata):
        '''
        Execute this state
        '''
        text = userdata.ParamName
        if rospy.has_param(userdata.ParamName):
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
                    print("\t" + str(match[+1:]))
                    ok = False
            print("by \"" + text + "\"")
            userdata.Value = text
            return "done"

        return "failed"