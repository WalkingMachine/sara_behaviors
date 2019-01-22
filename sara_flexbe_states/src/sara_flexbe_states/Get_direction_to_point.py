from flexbe_core import EventState, Logger
from wm_direction_to_point.srv import get_direction, get_directionRequest
import rospy

class Get_direction_to_point(EventState):

    '''
    Gets the direction to a given point. Receives an input_key: point
    and has 2 parameters : frame_reference and frame_origin. Returns 2 angles within userdata.

    -- frame_reference  string         Name for the frame the targetPoint is compared to
    -- frame_origin     string         Name for the frame, who will return an angle

    ># targetPoint      point          Position of the point.

    #> yaw              float64        Value of the yaw angle in the origin frame.
    #> pitch            float64        Value of the pitch angle in the origin frame.

    <= done                            Indicates completion of the calculation.
    <= fail                            Indicates it failed.

    '''



    def __init__(self, frame_origin, frame_reference):
        '''
        Constructor
        '''
        super(Get_direction_to_point, self).__init__(outcomes=['done','fail'], input_keys=['targetPoint'], output_keys=['yaw','pitch'])
        self.service = get_directionRequest()
        self.service.reference = frame_reference
        self.service.origine = frame_origin

        Logger.loginfo('waiting for service /get_direction')
        rospy.wait_for_service('/get_direction')    #Attend que le service soit disopnible

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        #rospy.wait_for_service('/get_direction')
        serv = rospy.ServiceProxy('/get_direction', get_direction)
        self.service.point = userdata.targetPoint
        resp = serv(self.service)

        userdata.yaw = resp.yaw
        userdata.pitch = resp.pitch

        Logger.loginfo('Angle retrieved')

        return 'done'