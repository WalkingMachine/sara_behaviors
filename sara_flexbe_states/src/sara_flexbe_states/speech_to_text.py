#!/usr/bin/env python
from flexbe_core import EventState, Logger
from std_msgs.msg import String

import rospy


class SpeechToText(EventState):
    '''
    Speech to text analyse mic audio file and output analysed word from it.

    #> words 		object 	Output the recognized speech.

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(SpeechToText, self).__init__(outcomes=['done', 'failed'],
                                            output_keys=['words'])

        self._start_time = None

        self._error = False
        self._stop = False

        self._topic = "/Stop"

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        self.check_stop()
        if self._error:
            return 'failed'

        # POCKET SPHINX ####
        #

        userdata.words = "Something that work!"
        Logger.loginfo('Execute.')

        return 'done'  # One of the outcomes declared above.

    def on_enter(self, userdata):
        # This method is called when the state becomes active, a transition from another state to this one is taken.
        # It is primarily used to start actions which are associated with this state.

        self.check_stop()
        Logger.loginfo('Enter STT')

    def check_stop(self):
        rospy.Subscriber(self._topic, String, self.callback)
        if self._stop:
            self._error = True
            Logger.logwarn('E-STOP ACTIVATED')

    def callback(self, stop):
        rospy.loginfo("E-STOP: %s", stop.data)
        self._stop = stop
        if stop:
            self._error = True
            Logger.logwarn('E-STOP ACTIVATED')
