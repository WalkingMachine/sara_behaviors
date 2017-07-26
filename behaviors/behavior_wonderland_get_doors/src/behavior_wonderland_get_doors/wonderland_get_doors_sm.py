#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_get_doors')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
from sara_flexbe_states.Wonderland_Get_Doors import Wonderland_Get_Doors
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 16 2017
@author: Lucas Maurice
'''
class Wonderland_Get_DoorsSM(Behavior):
	'''
	List all doors.
	'''


	def __init__(self):
		super(Wonderland_Get_DoorsSM, self).__init__()
		self.name = 'Wonderland_Get_Doors'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:747 y:521, x:517 y:516
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], output_keys=['exit_pose', 'entrance_id', 'entrance_pose', 'entrance_rooms_id', 'entrance_rooms_names', 'exit_id', 'exit_rooms_id', 'exit_rooms_names'])
		_state_machine.userdata.entrance_id = None
		_state_machine.userdata.entrance_pose = None
		_state_machine.userdata.entrance_rooms_id = None
		_state_machine.userdata.entrance_rooms_names = None
		_state_machine.userdata.exit_id = None
		_state_machine.userdata.exit_pose = None
		_state_machine.userdata.exit_rooms_id = None
		_state_machine.userdata.exit_rooms_names = None
		_state_machine.userdata.url = "door"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:241 y:68
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'Wonderland_Get_Doors', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'entity'})

			# x:508 y:67
			OperatableStateMachine.add('Wonderland_Get_Doors',
										Wonderland_Get_Doors(),
										transitions={'done': 'done', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'entity', 'entrance_id': 'entrance_id', 'entrance_pose': 'entrance_pose', 'entrance_rooms_id': 'entrance_rooms_id', 'entrance_rooms_names': 'entrance_rooms_names', 'exit_id': 'exit_id', 'exit_pose': 'exit_pose', 'exit_rooms_id': 'exit_rooms_id', 'exit_rooms_names': 'exit_rooms_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
