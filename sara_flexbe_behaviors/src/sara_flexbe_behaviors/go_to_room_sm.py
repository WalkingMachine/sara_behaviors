#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_go_to_room')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_move_base import SaraMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 28 2017
@author: Redouane Laref
'''
class Go_To_RoomSM(Behavior):
	'''
	Go To the entity room.
	'''


	def __init__(self):
		super(Go_To_RoomSM, self).__init__()
		self.name = 'Go_To_Room'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:938 y:315, x:130 y:302
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name', 'index'])
		_state_machine.userdata.name = ""
		_state_machine.userdata.index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:236 y:55
			OperatableStateMachine.add('Wait_time',
										WaitState(wait_time=3),
										transitions={'done': 'Wonderland_Get_Entity'},
										autonomy={'done': Autonomy.Off})

			# x:748 y:182
			OperatableStateMachine.add('Move to object',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'waypoint_pose'})


			# x:685 y:73
			OperatableStateMachine.add('read',
										Wonderland_Read_Entity(index_function=lambda x: 0),
										transitions={'done': 'Move to object', 'empty': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'entity', 'input_value': 'name', 'id': 'id', 'name': 'name', 'time': 'time', 'x_pos': 'x_pos', 'y_pos': 'y_pos', 'z_pos': 'z_pos', 'waypoint_id': 'waypoint_id', 'waypoint_pose': 'waypoint_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
