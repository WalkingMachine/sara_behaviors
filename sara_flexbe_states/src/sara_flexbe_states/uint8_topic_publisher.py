#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy

from flexbe_core.proxy import ProxyPublisher
from std_msgs.msg import UInt8


class PublishUint8(EventState):
    '''
    Publishes a uint 8 on a topic.


    ># data uint8		uint8 to publish.
    ># topic    string       topic to publish on.
    <= done            uint8 has been published.

    '''

    def __init__(self):

        super(PublishUint8, self).__init__(input_keys=['topic', 'data'], outcomes=['done'])


    def on_enter(self, userdata):
        Logger.loginfo('Entering uint8 publisher')

    def execute(self, userdata):

        pub = rospy.Publisher(userdata.topic, UInt8, queue_size=10)

        pub.publish(userdata.data)

        Logger.loginfo('Publishing done')
        return 'done'
