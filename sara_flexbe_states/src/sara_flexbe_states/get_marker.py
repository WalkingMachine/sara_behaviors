#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from tf.transformations import quaternion_from_euler, quaternion_matrix, quaternion_from_matrix
from geometry_msgs.msg import Quaternion
import rostopic
import inspect
from rospy.rostime import get_time

class GetMarker(EventState):
    '''
    Gets the pose of a AR marker.

    -- index  index of the marker.


    #> pose         geometry_msgs.Pose        Current pose of the AR marker.

    <= done         The pose is received.
    <= not_found         The marker is not found

    '''

    def __init__(self, index):
        '''
        Constructor
        '''
        super(GetMarker, self).__init__(outcomes=['done', 'not_found'], output_keys=['pose'])
        self.index = index
        self._topic = "/ar_pose_marker"
        self._connected = False

        (msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)


        if msg_topic == self._topic:
            msg_type = self._get_msg_from_path(msg_path)
            self._sub = ProxySubscriberCached({self._topic: msg_type})
            self._connected = True

            Logger.loginfo('connecting marker state to '+self._topic)
        else:
            Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

        self.quat = quaternion_from_euler(0, 0, -3.14159/2)
        #self.mat = quaternion_matrix(quat)

    def execute(self, userdata):
        '''
        Execute this state
        '''



        Logger.loginfo('looking for marker ' + str(self.index))
        if not self._connected:
            return 'not_found'


        if self._sub.has_msg(self._topic):
            message = self._sub.get_last_msg(self._topic)

            #Logger.loginfo(str(message))
            #Logger.loginfo('there is ' + str(len(message.markers))+' in the list')

            for marker in message.markers:

                Logger.loginfo('id is ' + str(marker.id))

                if int(marker.id) == int(self.index):
                    # pose = []
                    # pose.append(marker.pose.pose.orientation.w)
                    # pose.append(marker.pose.pose.orientation.x)
                    # pose.append(marker.pose.pose.orientation.y)
                    # pose.append(marker.pose.pose.orientation.z)
                    #
                    # quat = self.quat
                    # marker.pose.pose.position.x -= 0.20
                    # marker.pose.pose.position.z += 0.05
                    # marker.pose.pose.orientation.x = -0.460612186114
                    # marker.pose.pose.orientation.y = -0.46897814506
                    # marker.pose.pose.orientation.z = 0.501742587173
                    # marker.pose.pose.orientation.w = 0.56227243368
                    userdata.pose = marker.pose.pose
                    self._sub.remove_last_msg(self._topic)
                    return 'done'

            return 'not_found'

        time = self.time - get_time()+5
        Logger.loginfo('marker not found '+str(int(time))+' before giving up')
        if (time <= 0):
            return 'not_found'



    def on_enter(self, userdata):
        Logger.loginfo('entering marker state')

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
