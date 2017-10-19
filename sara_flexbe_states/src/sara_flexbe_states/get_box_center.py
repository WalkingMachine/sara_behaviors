#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from tf.transformations import quaternion_from_euler, quaternion_matrix, quaternion_from_matrix
from geometry_msgs.msg import Quaternion
import rostopic
import inspect
from rospy.rostime import get_time

class GetBoxCenter(EventState):
    '''
    Temporary feature: Gets the center point of a box given by frame_to_box.

    -- name  name of the box.


    #> point         geometry_msgs.Point        center of the box

    <= done         The point is received.
    <= not_found         The box is not found

    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        super(GetBoxCenter, self).__init__(outcomes=['done', 'not_found'], output_keys=['point'])
        self.Class = name
        self._topic = "/frame_to_boxes/bounding_boxes"
        self._connected = False

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)


        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True

            Logger.loginfo('connecting box state to '+self._topic)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

        self.quat = quaternion_from_euler(0, 0, -3.14159/2)
        #self.mat = quaternion_matrix(quat)

    def execute(self, userdata):
        '''
        Execute this state
        '''



        Logger.loginfo('looking for box ' + str(self.Class))
        if not self._connected:
            return 'not_found'


        if self._sub.has_msg(self._topic):
            message = self._sub.get_last_msg(self._topic)


            Logger.loginfo('getting message')
            for box in message.boundingBoxes:

                Logger.loginfo('name is ' + str(box.Class))

                if str(box.Class) == str(self.Class):
                    userdata.point = box.Center
                    self._sub.remove_last_msg(self._topic)
                    return 'done'


        time = self.time - get_time()+5
        Logger.loginfo('box not found '+str(int(time))+' before giving up')
        if (time <= 0):
            return 'not_found'



    def on_enter(self, userdata):
        Logger.loginfo('entering boxes state')

        self.time = get_time()
        if not self._connected:
            (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
            if msg_topic == self._topic:
                msg_type = self._get_msg_from_path(msg_path)
                self._sub = ProxySubscriberCached({self._topic: msg_type})
                self._connected = True
                Logger.loginfo('Successfully subscribed to previously unavailable topic %s' % self._topic)
            else:
                Logger.logwarn('Topic %s still not available, giving up.' % self._topic)



    def _get_msg_from_path(self, msg_path):
        msg_import = msg_path.split('/')
        msg_module = '%s.msg' % (msg_import[0])
        package = __import__(msg_module, fromlist=[msg_module])
        clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
        return clsmembers[0][1]
