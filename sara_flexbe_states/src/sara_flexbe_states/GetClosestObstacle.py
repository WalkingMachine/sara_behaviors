#!/usr/bin/env python

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from sensor_msgs.msg import LaserScan

class GetClosestObstacle(EventState):
    """
    Renvoie l'angle de l'obstacle le plus proche.

    ### InputKey
    ># angle        msg.ranges

    ### OutputKey
    <= done         Angle de l'obstacle
    """

    def __init__(self, topic="/scan", maximumDistance=2):
        '''
        Constructor
        '''
        super(GetClosestObstacle, self).__init__(outcomes=['done'], output_keys=['Angle'])

        self._topic = topic
        self._sub = ProxySubscriberCached({self._topic: LaserScan})
        self.maximumDistance = maximumDistance

    def execute(self, userdata):
        '''
        Execute this state
        '''

        Angle = 0
        previousMinimum = self.maximumDistance
        i = 0

        msg = self._sub.get_last_msg(self._topic)
        # print(str(msg))
        if msg:
            for range in msg.ranges:
                if range < previousMinimum and range > 0.4:
                    previousMinimum = range
                    Angle = msg.angle_min + i * msg.angle_increment
                i += 1

            Logger.loginfo("closest obstacle is at "+str(Angle)+" and "+str(previousMinimum))

        userdata.Angle = max(min(Angle, 1.8), -1.8)
        return "done"