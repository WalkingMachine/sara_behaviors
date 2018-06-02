#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
from flexbe_core import EventState, Logger
import rospy
import re
from wm_nlu.srv import GPSRReceiveAction, GPSRReceiveActionResponse
from std_msgs.msg import String


class SaraNLUspr(EventState):
    '''
    Use wm_nlu to parse a sentence and return the detected actions in a standard format (ActionForm)

    ># sentence     string      sentence to parse

    #> ActionForms     string[]      list of ActionForms

    <= understood     Finished job.
    <= not_understood     Finished job but no commands detected.
    <= fail     service unavailable.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(SaraNLUspr, self).__init__(outcomes=['understood', 'not_understood', 'fail'], input_keys=['sentence'],
                                      output_keys=['ActionForms'])
        self.RecurentSubject = None
        self.Person = None
        self.serviceName = "/answer_question"

        Logger.loginfo("waiting forservice: " + self.serviceName)
        rospy.wait_for_service(self.serviceName)

    def execute(self, userdata):

        # Special case for STOP
        regex = re.compile('.*(stop).*')
        if regex.match(userdata.sentence.lower()):
            Logger.loginfo("Stop now!")
            userdata.ActionForms = [["Stop"]]
            return "understood"

        # Call the NLU service
        serv = rospy.ServiceProxy(self.serviceName, GPSRReceiveAction)
        Resp = serv(String(userdata.sentence))

        # Checking the validity of the responce
        count = len(Resp.actions.actions)
        Logger.loginfo("Action list - count : " + str(count))
        if count == 0:
            userdata.ActionForms = []
            return "not_understood"

        # Convert the ActionMsgArray into ActionForms
        ActionForms = []
        for Action in Resp.actions.actions:
            # create an ActionForm
            ActionForm = []
            ActionForm.append(Action.Action)
            for arg in Action.args:
                ActionForm.append(arg)

            # Add it to the list
            ActionForms.append(ActionForm)

        userdata.ActionForms = ActionForms

        return "understood"

    def on_enter(self, userdata):
        Logger.loginfo('Enter SaraNLU')
