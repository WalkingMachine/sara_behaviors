#!/usr/bin/env python
from flexbe_core import EventState, Logger
from sensor_msgs.msg import LaserScan
from flexbe_core.proxy import ProxySubscriberCached
from rospy.rostime import get_time

import rospy


class CupboardDoorDetector(EventState):
    '''
    Detect if door is open
    REF : https://github.com/WalkingMachine/wm_door_detector

    -- timeout  limit time before conclusion
    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, timeout):
        # See example_state.py for basic explanations.
        super(CupboardDoorDetector, self).__init__(outcomes=['open', 'closed'])

        self.distances = []
        self._topic = "/scan"
        self._sub = ProxySubscriberCached({self._topic: LaserScan})
        self.time = 0
        self.timeout = timeout

    def avg(self, lst):
        return sum(lst) / max(len(lst), 1)

    def interval(self, lst):
        return max(lst)-min(lst)

    def process_scan(self, scan_msg):

        # Extract the interval in a restricted range to determine if the is a closed door
        middle_index = len(scan_msg.ranges)/2
        ranges_at_center = scan_msg.ranges[middle_index-40:middle_index+40]
        interval_of_door = self.interval(ranges_at_center)

        print( "dist = "+str(interval_of_door))
        if interval_of_door < 0.1 or interval_of_door > 0.5 or max(ranges_at_center) > 0.85:
            rospy.loginfo("Distance to door is more than a meter")
            return "open"

        if (self.time-get_time() <= 0):
            Logger.loginfo('no speech detected')
            return 'closed'

    def execute(self, userdata):
        if self._sub.has_msg(self._topic):
            message = self._sub.get_last_msg(self._topic)
            return self.process_scan(message)

    def on_enter(self, userdata):
        rospy.loginfo("Waiting for door...")
        self.time = get_time()+self.timeout

    def on_exit(self, userdata):
        rospy.loginfo("The door is now open")

