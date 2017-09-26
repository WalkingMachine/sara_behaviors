#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from geometry_msgs.msg import Pose, Point, Quaternion
from tf import transformations

import rospy
import rostopic
import inspect

import json


class Get_Robot_Pose(EventState):
    '''
	Gets the latest message on the given topic and stores it to userdata.

	-- topic 		string		The topic on which should be listened.
	-- blocking 	bool 		Blocks until a message is received.
	-- clear 		bool 		Drops last message on this topic on enter
								in order to only handle message received since this state is active.

	#> pose		Pose2D		    Latest message on the given topic of the respective type.

	<= done 				Message has been received and stored in userdata or state is not blocking.
	<= failed 				The topic is not available when this state becomes actives.

	'''

    def __init__(self, blocking=True, clear=False):
        '''
		Constructor
		'''
        super(Get_Robot_Pose, self).__init__(outcomes=['done', 'failed'],
                                             output_keys=['pose'])

        self._topic = "/robot_pose"
        self._blocking = blocking
        self._clear = clear
        self._connected = False

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)

        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True
        else:
            Logger.logwarn(
                'Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (
                    self._topic, self.name, str(msg_topic)))

    def execute(self, userdata):
        '''
		Execute this state
		'''
        if not self._connected:
            return 'failed'

        if self._sub.has_msg(self._topic) or not self._blocking:
            userdata.pose = self._sub.get_last_msg(self._topic)
            self._sub.remove_last_msg(self._topic)
            return 'done'

    def on_enter(self, userdata):
        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
            if msg_topic == self._topic:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic)
            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic)

        if self._connected and self._clear and self._sub.has_msg(self._topic):
            self._sub.remove_last_msg(self._topic)

    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(
            msg_import[1]))
        return clsmembers[0][1]
