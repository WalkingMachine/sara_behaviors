#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_get_robot_pose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Nicolas Nadeau
'''
class Get_Robot_poseSM(Behavior):
	'''
	Get the current position of the robot
	'''


	def __init__(self):
		super(Get_Robot_poseSM, self).__init__()
		self.name = 'Get_Robot_pose'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:182 y:161
			OperatableStateMachine.add('Position',
										Get_Robot_Pose(blocking=True, clear=False),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
