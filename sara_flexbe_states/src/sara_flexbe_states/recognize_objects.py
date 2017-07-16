#!/usr/bin/env python
import actionlib
import rospy
from sensor_msgs.msg import Image
from object_recognition_msgs.msg import ObjectRecognitionAction, ObjectRecognitionGoal
from flexbe_core import EventState, Logger


class ObjectsRecognize(EventState):
    '''
    ObjectsRecognize finds requested object and returns its position in the space

    #> image     Image                   Scene where objects are recognized

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def on_result(status, result):
        print result

    def __init__(self):
        # See example_state.py for basic explanations.
        super(ObjectsRecognize, self).__init__(outcomes=['done', 'failed'], output_keys=['image'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        Logger.loginfo('Waiting for ORK detector')

        # Retrieve image to add bounding boxes to it
        Logger.loginfo("Wait for image")
        image_msg = rospy.wait_for_message("/camera/rgb/image_rect_color", Image,
                                           30)  # for kinect2 : '/kinect2/qhd/image_color_rect' for xtion : '/camera/rgb/image_rect_color'
        try:
            userdata.image = image_msg
            Logger.loginfo("Image received")
        except rospy.ROSException, e:
            Logger.loginfo("Time out")

        # Run ORK actionlib
        client = actionlib.SimpleActionClient('recognize_objects', ObjectRecognitionAction)
        Logger.loginfo('client done')
        client.wait_for_server()
        Logger.loginfo('Waiting server')
        goal = ObjectRecognitionGoal()
        client.send_goal(goal, done_cb=self.on_result)
        client.wait_for_result()  # wait indefinitely for a result

        Logger.loginfo('The scene should have been recognized')

        return 'done'  # One of the outcomes declared above.
