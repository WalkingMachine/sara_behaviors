#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
import rospy
from wm_nlu.srv import PHGetObject
from std_msgs.msg import String

class SaraNLUgetObject(EventState):
    '''
    Use wm_nlu to parse a sentence and return an object for the 2019 Where Is This Challenge

    ># sentence     string      sentence to parse
    
    #> object     string      object string
    
    <= understood     Finished job.
    <= not_understood     Finished job but no commands detected.
    <= fail     service unavailable.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(SaraNLUgetObject, self).__init__(outcomes=['understood', 'not_understood', 'fail'], input_keys=['sentence'],output_keys=['answer'])

        serviceName = "/get_object"

        Logger.loginfo("waiting for service: "+serviceName)
        rospy.wait_for_service(serviceName)

        self.service = rospy.ServiceProxy(serviceName, PHGetObject)

    def execute(self, userdata):

        # Call the NLU service
        response = self.service(String(userdata.sentence))

        # Checking the validity of the response
        if response.str.data == "" or response.str.data == "none":
            userdata.answer = response.str.data
            return "fail"

        userdata.answer = response.str.data
        return "understood"
