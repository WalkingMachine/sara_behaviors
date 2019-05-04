#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
import rospy
from wm_nlu.srv import ReceptionistNLUService
from std_msgs.msg import String


class SaraNLUreceptionist(EventState):
    '''
    Use wm_nlu to parse a sentence and return the answer.
    ># sentence         string      sentence to parse
    #> answer           string      answer

    <= understood       Finished job.
    <= not_understood   Finished job but no commands detected.
    <= fail     Finished job but sentence not successfully parsed or service unavailable.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(SaraNLUreceptionist, self).__init__(outcomes=['understood', 'fail'], input_keys=['sentence'],
                                         output_keys=['answer'])

        serviceName = "/receptionist_NLU"

        Logger.loginfo("waiting forservice: " + serviceName)
        rospy.wait_for_service(serviceName)

        self.service = rospy.ServiceProxy(serviceName, ReceptionistNLUService)

    def execute(self, userdata):

        # Call the NLU service
        response = self.service(String(userdata.sentence))

        # Checking the validity of the response
        if response.str.data is "unknown":
            userdata.answer = response.str.data
            return "fail"

        if response.str.data is "":
            userdata.answer = response.str.data
            return "fail"

        userdata.answer = response.str.data
        return "understood"
