#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from std_msgs.msg import UInt8


class SetExpression(EventState):
    '''
    State en python changeant l'expression et la luminosite du visage de Sara.
    @author Raphael Duchaine
    @license Apache2.0

    -- emotion      uint8   emotion to publish.[1-7](0 is no_change)
    -- brightness   uint8   brightness to publish[0-255](>255 is no_change)
    <= done                 emotion and brightness were published.
    '''

#enum [no_change, smile, sad, straight_mouth, angry, surprise, blink, party]

    def __init__(self, emotion, brightness):
        super(SetExpression, self).__init__(outcomes=['done'])
        self.emotion=emotion
        self.brightness=brightness

    def on_enter(self, userdata):
        Logger.loginfo('Entering Set_Expression')

    def execute(self, userdata):
        if(self.emotion>0):
        #Publish the emotion on topic "sara_face/Emotion" with a UInt8.
        #1 = smile, 2 = sad, 3 = straight mouth, 4 = angry, 5 = surprise, 6 = blink, 7 = party
            emotion_topic = "sara_face/Emotion"
            pub = rospy.Publisher(emotion_topic, UInt8, queue_size=1)
            pub.publish(self.emotion)
            Logger.loginfo('Emotion publishing done')
        #Brightness can be set (0-255) by sending the value on topic "sara_face/Brightness" with a UInt8.
        if(self.brightness<256 and self.brightness>0):
            face_brightness_topic = "sara_face/Brightness"
            pub = rospy.Publisher(face_brightness_topic, UInt8, queue_size=1)
            pub.publish(self.brightness)
            Logger.loginfo('Brightness publishing done')

        return 'done'
