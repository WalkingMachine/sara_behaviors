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

        self.serviceName = '/get_direction'
        Logger.loginfo('waiting for service /get_direction')

        self._active = True
        self.serv = rospy.ServiceProxy(self.serviceName, get_direction)
        try:
            self.serv.wait_for_service(1)
        except:
            self._active = False

    def on_enter(self, userdata):
        if self._active:
            self.service.point = userdata.targetPoint
            resp = self.serv(self.service)

            userdata.yaw = resp.yaw
            userdata.pitch = resp.pitch

            Logger.loginfo('Angle retrieved')
        else:
            userdata.yaw = 0
            userdata.pitch = 0


    def execute(self, userdata):
        return 'done'
