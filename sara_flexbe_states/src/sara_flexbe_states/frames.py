# !/usr/bin/env python

from flexbe_core import EventState
import rospy
import tf
import tf2_ros
import tf2_msgs.msg
import geometry_msgs.msg
import math
import roslib

roslib.load_manifest('learning_tf')


class frames(EventState):
    """
        Make sara point something

    -- target         int      what to point


    <= done                what's has to be pointed is pointed
    """

    def __init__(self):
        """Constructor"""
        rospy.init_node('frame_test')

        listener = tf.TransformListener()
        broadcaster = tf.TransformBroadcaster()
        rate = rospy.Rate(10.0)  # Run this loop at about 10Hz
        while not rospy.is_shutdown():

            print("ok1")
            """Coordinates"""
            x = 0
            y = 2
            z = 0

            broadcaster.sendTransform((x, y, z),
                                      tf.transformations.quaternion_from_euler(0, 0, 0),
                                      rospy.Time.now(),
                                      "target",
                                      "base_link")

            print("ok2")
            try:
                (trans, rot) = listener.lookupTransform('base_link', 'right_robotiq_arg2f_link', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            # calcul pour avoir les angles
            angular = math.atan2(trans[1], trans[0])
            linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            angular2 = math.atan2((y - trans[1]), (x - trans[0]))

            print('angle = ' + str(angular))
            print('angle = ' + str(angular2))

            broadcaster.sendTransform((math.cos(angular2), math.sin(angular2), 0),
                                      tf.transformations.quaternion_from_euler(0, 0, 0),
                                      rospy.Time.now(),
                                      "target2",
                                      "target")

            rate.sleep()


if __name__ == '__main__':
    frames()
