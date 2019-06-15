#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
import rospy
from wm_nlu.srv import HKGetRoom
from std_msgs.msg import String


class SaraNLUgetRoom(EventState):
    '''
    Use wm_nlu to parse a sentence and return a room

    ># sentence     string      sentence to parse
    
    <= understood     Finished job.
    <= not_understood     Finished job but no commands detected.
    <= fail     service unavailable.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(SaraNLUgetRoom, self).__init__(outcomes=['understood', 'not_understood', 'fail'],
                                             input_keys=['sentence'],
                                             output_keys=['answer'])

        serviceName = "/get_room"

        Logger.loginfo("waiting for service: "+serviceName)
        rospy.wait_for_service(serviceName)

        self.service = rospy.ServiceProxy(serviceName, HKGetRoom)

    def execute(self, userdata):

        # Call the NLU service
        response = self.service(String(userdata.sentence))

        # Checking the validity of the response
        if response.str.data is "" or "none":
            userdata.answer = response.str.data
            return "not_understood"

        userdata.answer = response.str.data
        return "understood"
