
import rospy
from sara_msgs import msg
from flexbe_core import EventState, Logger

class handleBag(EventState):
    '''
    ALlows the user to get a pointcloud of the handle

    -- handle  function         ALlows the user to get a pointcloud of the handle /sort data

    ># input_list  list        Input to the filter function

    #> output_PointCloud PointCloud    The result of the filter.

    <= done                    Indicates completion of the filter.

    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(handleBag,self).__init__(outcomes=['does_have_handle','does_not_have_handle'],input_keys=['entity'])


    def execute(self,userdata):

        if (len(userdata.entity.pointcloud.data)):
            return "does_have_handle"
        else:
            return "does_not_have_handle"
