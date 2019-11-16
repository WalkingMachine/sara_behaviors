#!/usr/bin/env python

from flexbe_core.proxy import ProxyPublisher
from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core.proxy import ProxyServiceCaller
# from flexbe_core.proxy import ProxyActionClient # TODO utiliser le action server a la place du service
from flexbe_core import EventState, Logger
import rospy
from wm_tts.msg import say
from wm_tts.srv import say_service, say_serviceRequest
from std_msgs.msg import UInt8
import types
import random

class SaraSay(EventState):
    """
    Make sara say something

    -- sentence      string      What to say.
                                 Can be a simple String, a list of strings from which one will be randomly picked 					 or a lambda function using input_keys.
                                 (e.g., lambda x: "I found the "x[0] + " on the " + x[1] + "!").
    -- input_keys    string[]    List of available input keys.
    -- emotion       int         Set the facial expression.
                                 (0=no changes, 1=happy, 2=sad, 3=straight mouth, 4=angry, 5=surprise, 6=blink, 7=party)
    -- block         Bool        Should the robot finish it's sentence before continuing?

    ># input_keys   object[]     Input(s) to the sentence as a list of userdata.
                                 The individual inputs can be accessed as list elements (see lambda expression example).

    <= done                      what's said is said
    """

    def __init__(self, sentence, input_keys=[], emotion=0, block=True):
        """Constructor"""

        super(SaraSay, self).__init__(outcomes=['done'], input_keys=input_keys)

        if not (isinstance(sentence, types.LambdaType) and sentence.__name__ == "<lambda>") and len(input_keys) is not 0:
            raise ValueError("In state " + type(
                                 self).__name__ + " saying \"" + sentence + "\", you need to define a lambda function for sentence.")

        # Get parameters
        self.msg = say()
        self.sentence = sentence
        self.emotion = UInt8()
        self.emotion.data = emotion
        self.block = block

        # Set topics
        self.emotion_topic = "sara_face/Emotion"
        self.say_topic = "/say"
        self.sayServiceTopic = "/wm_say"
        self.emotionPub = ProxyPublisher({self.emotion_topic: UInt8})

        # Prepare wm_tts
        if self.block:
            self.sayClient = ProxyServiceCaller({self.sayServiceTopic: say_service})
        else:
            self.sayPub = ProxyPublisher({self.say_topic: say})

        # Initialise the face sub
        self.emotionSub = ProxySubscriberCached({self.emotion_topic: UInt8})
        self.lastEmotion = None

    def execute(self, userdata):
        if self.block:
            if self.sayClient.is_available(self.sayServiceTopic):
                try:
                    # Call the say service
                    srvSay = say_serviceRequest()
                    srvSay.say.sentence = self.msg.sentence
                    srvSay.say.emotion = self.msg.emotion
                    self._response = self.sayClient.call(self.sayServiceTopic, srvSay)
                except rospy.ServiceException as exc:
                    Logger.logwarn("Sara say did not work: \n" + str(exc))

                return 'done'
            else:
                Logger.logwarn("wm_tts service is not available. Remaining trials: " + str(self.maxBlockCount))
                # Count the number of trials before continuing on life
                self.maxBlockCount -= 1
                if self.maxBlockCount <= 0:
                    return 'done'
        else:
            return 'done'

    def on_enter(self, userdata):
        if self.emotion.data is not 0:
            # Save the previous emotion so we can place it back later
            if self.block and self.emotionSub.has_msg(self.emotion_topic):
                self.lastEmotion = self.emotionSub.get_last_msg(self.emotion_topic)
                self.emotionSub.remove_last_msg(self.emotion_topic)

            # Set the emotion
            self.emotionPub.publish(self.emotion_topic, self.emotion)

        # Set the message according to the lambda function if needed.
	#If there is a list of messages, one of the messages will be picked at random.
        if isinstance(self.sentence, types.LambdaType) and self.sentence.__name__ == "<lambda>":
            self.msg.sentence = self.sentence(map(lambda key: userdata[key], list(reversed(list(self._input_keys)))))
        elif not isinstance(self.sentence, basestring):
		self.msg.sentence=self.sentence[random.randint(0,len(self.sentence))]
	else:
            self.msg.sentence = self.sentence
	


        Logger.loginfo('Sara is saying: "' + str(self.msg.sentence) + '".')

        # Say the thing if not blocking
        if not self.block:
            # publish
            self.sayPub.publish(self.say_topic, self.msg)
            return "done"

        # Set the maximum tries before continuing
        self.maxBlockCount = 30

    def on_exit(self, userdata):
        if self.block and self.emotion.data is not 0:
            # Put the original emotion back
            if self.lastEmotion:
                self.emotionPub.publish(self.emotion_topic, self.lastEmotion)
