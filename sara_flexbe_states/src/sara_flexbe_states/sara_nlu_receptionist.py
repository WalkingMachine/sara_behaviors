#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from flexbe_core import EventState, Logger
import rospy
from wm_nlu.srv import ReceptionistNLUService, ReceptionistNLUServiceRequest


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

        self.serviceName = "/Receptionist_NLU_Service"

        Logger.loginfo("waiting forservice: " + self.serviceName)

        self.serviceNLU = ProxyServiceCaller({self.serviceName: ReceptionistNLUService})
        # self.service = rospy.ServiceProxy(serviceName, ReceptionistNLUService)

    def execute(self, userdata):

        if self.serviceNLU.is_available(self.serviceName):

            try:
                # Call the say service
                srvRequest = ReceptionistNLUServiceRequest()
                srvRequest.str = userdata.sentence
                response = self.serviceNLU.call(self.serviceName, srvRequest)

                if not response:
                    userdata.answer = "unknown"
                    return "fail"

                # Checking the validity of the response
                if response.response is "unknown":
                    userdata.answer = response.response
                    return "fail"

                if response.response is "":
                    userdata.answer = "unknown"
                    return "fail"

                userdata.answer = response.response
                return "understood"

            except rospy.ServiceException as exc:
                Logger.logwarn("Receptionist NLU did not work: \n" + str(exc))
