#!/usr/bin/env python
from flexbe_core import EventState, Logger
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from threading import Event

import sqlite3
import roslib
import rospy


class DoorDetector(EventState):
    '''
    Detect if door is open
    REF : https://github.com/WalkingMachine/wm_door_detector

    -- timeout  Max wait for a door detection (in sec)

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self, timeout):
        # See example_state.py for basic explanations.
        super(DoorDetector, self).__init__(outcomes=['done', 'failed'])

        self.distances = []
        self.door_open = Event()
        self.timeout = timeout
        self.no_door_found = False
        self._error = False

    def avg(self, lst):
        return sum(lst) / max(len(lst), 1)

    def process_scan(self, scan_msg):
        try:
            middle_index = len(scan_msg.ranges)/2
            ranges_at_center = scan_msg.ranges[middle_index-2:middle_index+2]
            distance_to_door = self.avg(ranges_at_center)
            self.distances += [distance_to_door]

            avg_distance_now = self.avg(self.distances[-5:])

            if self.distances[0] > 1.0:
                self.no_door_found = True
                rospy.loginfo("No door found")
                self.door_open.set()
            elif avg_distance_now > 1.0:
                rospy.loginfo("Distance to door is more than a meter")
                self.door_open.set()

        except:
            rospy.logerr("Fail sub to laser")
            self.laser_sub.unregister()
            self._error = True
            Logger.loginfo('Fail sub to laser')
            return 'failed'

    def execute(self, userdata):
        rospy.loginfo("Waiting for door...")
        laser_sub = rospy.Subscriber("/scan", LaserScan, self.process_scan)
        door_pub = rospy.Publisher('/door', String, queue_size=10)

        opened_before_timeout = self.door_open.wait(timeout=self.timeout)

        rospy.loginfo("Unregistering laser and clearing data")
        laser_sub.unregister()
        self.distances = []

        self.door_open.clear()

        if self.no_door_found:
            rospy.loginfo("No door found")
            door_pub.publish("no_door")
            Logger.loginfo('Fail sub to laser')
            return 'failed'

        if opened_before_timeout:
            rospy.loginfo("Door is open")
            door_pub.publish("open")
            return 'done'

        rospy.loginfo("timed out with door still closed")

        return 'failed'
