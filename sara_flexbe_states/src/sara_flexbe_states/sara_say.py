#!/usr/bin/env python

from flexbe_core.proxy import ProxyPublisher
from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core.proxy import ProxyServiceCaller
from flexbe_core.proxy import ProxyActionClient

import rospy

from flexbe_core import EventState, Logger

from wm_tts.msg import say
from wm_tts.srv import say_service, say_serviceRequest
from std_msgs.msg import UInt8

class SaraSay(EventState):
    """
    Make sara say something

    -- Format      string   how to say it
    -- emotion     int       how to feel
    >= sentence              what key to say

    <= done                what's said is said
    """

    def __init__(self, sentence, emotion, block=True):
        """Constructor"""

        super(SaraSay, self).__init__(outcomes = ['done'])

        # Get parameters
        self.msg = say()
        self.msg.sentence = sentence
        self.msg.emotion = emotion
        self.block = block
        self.lastEmotion = None

        # Set topics
        self.emotion_topic = "sara_face/Emotion"
        self.say_topic = "/say"
        self.say_service = "/wm_say"
        self.emotion_pub = ProxyPublisher({self.emotion_topic: UInt8})

        # Prepare wm_tts
        if self.block:
            Logger.loginfo('Waiting for wm_tts')
            rospy.wait_for_service(self.say_service)
            self.serv = ProxyServiceCaller({self.say_service: say_service})
        else:
            self.pub = ProxyPublisher({self.say_topic: say})

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        if(self.msg.emotion>0 and self.msg.emotion != self.lastEmotion):
            self.emotion_pub.publish(self.emotion_topic, self.msg.emotion)
            self.lastEmotion = self.msg.emotion

        Logger.loginfo('Say: '+str(self.msg))
        if self.block: # call service
            try:
                message_say = say_serviceRequest()
                message_say.say.sentence = self.msg.sentence
                message_say.say.emotion = self.msg.emotion
                self._response = self.serv.call(self.say_service, message_say)
            except rospy.ServiceException as exc:
                Logger.logwarn("Execute did not process request: \n" + str(exc))

        else: #publisher
            self.pub.publish(self.say_topic, self.msg)

        return 'done'
