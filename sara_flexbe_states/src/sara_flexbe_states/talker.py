
import rospy
from sara_msgs import msg
from flexbe_core import EventState, Logger
import ros_numpy
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
            xyz_array=ros_numpy.point_cloud2.point_cloud2_to_xyz_array(userdata.entity.pointcloud)
            xyz_array=np.mean(xyz_array)
            return xyz_array
        else:
            return "does_not_have_handle"
