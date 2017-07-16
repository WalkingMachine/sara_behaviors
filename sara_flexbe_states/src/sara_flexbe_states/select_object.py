#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2, Image
from geometry_msgs.msg import PoseWithCovarianceStamped
from object_recognition_msgs.msg import *
from wm_object_selection.srv import *
from object_recognition_msgs.msg import *
from flexbe_core import EventState, Logger



class ObjectSelect(EventState):
    '''
    ObjectSelect finds requested object and returns its position in the space

    ># object_name    String                   Object to find
    ># image          Image                    Image of the scene where objects are recognized
    ># objects_array  RecognizedObjects[]      List of all the recognized objects
    #> pose           Pose                     Pose of the requested object

    <= done     Finish job.
    <= failed   Job as failed.
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(ObjectSelect, self).__init__(outcomes=['done', 'failed', 'looping'], input_keys=['objects_array',
                                                                                    'object_name',
                                                                                    'image'], output_keys=['pose'])

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.
        # Initialize node
        rospy.logout("Fetch client initialized")
        # Create publisher for selected object_pose
        pub_object_pose = rospy.Publisher("/WMObjectProcessor/selected_object_pose",
                                          PoseWithCovarianceStamped,
                                          queue_size=100)
        # Build request
        req = RecognizeObjectRequest()
        req.filter = userdata.object_name
        req.image = userdata.image
        req.objectarray = userdata.objects_array

        Logger.loginfo('Waiting for slct_obj')
        rospy.wait_for_service('slct_obj')

        Logger.loginfo('Looking for '+req.filter)
        try:
            inputs_srv = rospy.ServiceProxy('slct_obj', RecognizeObject)
            slct_obj = inputs_srv(req)
            Logger.loginfo(
                'Service found the requested object at\n\r ' +
                str(slct_obj.selected_object_pose))
            pub_object_pose.publish(slct_obj.selected_object_pose)
            userdata.pose = slct_obj.selected_object_pose
            return 'done'  # One of the outcomes declared above.

        except rospy.ServiceException as e:
            if str(e).find('list index out of range'):
                Logger.loginfo('Service did not find the requested object, looping again')
                return 'looping'  # Return the outcome
            else:
                rospy.logerr('Service call failed: ' + str(e))
                return 'failed'  # Return the outcome

        Logger.loginfo('The detection is done')
