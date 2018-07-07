#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
from wm_tts.msg import say
from wm_tts.srv import say_service
from std_msgs.msg import UInt8

class SaraSayKey(EventState):
    """
    Make sara say something

    -- Format      string   how to say it
    -- emotion     int       how to feel
    >= sentence              what key to say

    <= done                what's said is said
    """

    def __init__(self, Format , emotion, block=True):
        """Constructor"""

        super(SaraSayKey, self).__init__(outcomes = ['done'],
                                      input_keys=['sentence'])
        self.Format = Format


        # Get parameters
        self.msg = say()
        self.msg.emotion = emotion
        self.block = block
        self.lastEmotion = None

        # Set topics
        self.emotion_topic = "sara_face/Emotion"
        self.say_topic = "/say"
        self.say_service = "/wm_say"
        self.emotion_pub = rospy.Publisher(self.emotion_topic, UInt8, queue_size=1)

        # Prepare wm_tts
        if self.block:
            Logger.loginfo('Waiting for wm_tts')
            rospy.wait_for_service(self.say_service)
            self.serv = rospy.ServiceProxy(self.say_service, say_service)
        else:
            self.pub = rospy.Publisher(self.say_topic, say, queue_size=1)

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        self.msg.sentence = str(self.Format( userdata.sentence ))
        if(self.msg.emotion>0 and self.msg.emotion != self.lastEmotion):
            self.emotion_pub.publish(self.msg.emotion)
            self.lastEmotion = self.msg.emotion

        Logger.loginfo('Say: '+str(self.msg))
        if self.block:
            self.serv(self.msg)
        else:
            self.pub.publish(self.msg)

        return 'done'
