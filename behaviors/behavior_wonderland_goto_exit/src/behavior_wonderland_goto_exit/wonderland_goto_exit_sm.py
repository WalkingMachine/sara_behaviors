#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_goto_exit')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_doors.wonderland_get_doors_sm import Wonderland_Get_DoorsSM
from flexbe_navigation_states.move_base_state import MoveBaseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Nicolas Nadeau
'''
class Wonderland_Goto_ExitSM(Behavior):
	'''
	Make SARA go to the exit door
	'''


	def __init__(self):
		super(Wonderland_Goto_ExitSM, self).__init__()
		self.name = 'Wonderland_Goto_Exit'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_DoorsSM, 'Wonderland_Get_Doors')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:858 y:113, x:717 y:474
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:199 y:116
			OperatableStateMachine.add('Wonderland_Get_Doors',
										self.use_behavior(Wonderland_Get_DoorsSM, 'Wonderland_Get_Doors'),
										transitions={'done': 'Move_SARA', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'exit_pose': 'exit_pose', 'entrance_id': 'entrance_id', 'entrance_pose': 'entrance_pose', 'entrance_rooms_id': 'entrance_rooms_id', 'entrance_rooms_names': 'entrance_rooms_names', 'exit_id': 'exit_id', 'exit_rooms_id': 'exit_rooms_id', 'exit_rooms_names': 'exit_rooms_names'})

			# x:652 y:143
			OperatableStateMachine.add('Move_SARA',
										MoveBaseState(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'exit_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
