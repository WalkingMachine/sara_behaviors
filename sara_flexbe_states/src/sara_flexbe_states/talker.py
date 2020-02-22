
import rospy
from sara_msgs import msg
from flexbe_core import EventState, Logger

class handleBag(EventState):
'''
    ALlows the user to get a pointcloud of the handle

    -- handle  function	     ALlows the user to get a pointcloud of the handle /sort data

    ># input_list  list		Input to the filter function

    #> output_PointCloud PointCloud	The result of the filter.

    <= done					Indicates completion of the filter.

    '''
	def __init__(self,handle):
		'''
	    Constructor
	    '''
		super(handle,self).__init__(outcomes=['found','notfound'],input_keys=['input_list'],output_keys=['output_PointCloud'])
	def handle(self, userdata):
		list=[]
		list = list.append(userdata.PointCloud)
		return list
	def execute(self,userdata):
		if(handle(userdata)!=0):
			Logger.loginfo('true')
		else:
			Logger.loginfo('false')
		return 'done'
