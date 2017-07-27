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
from behavior_wonderland_get_waypoint_from_id.wonderland_get_waypoint_from_id_sm import Wonderland_get_waypoint_from_idSM
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.Wonderland_Get_Waypoint import Wonderland_Get_Waypoint
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
		self.add_behavior(Wonderland_get_waypoint_from_idSM, 'Wonderland_get_waypoint_from_id')

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
										transitions={'done': 'Wonderland_get_waypoint_from_id'},
										autonomy={'done': Autonomy.Off})

			# x:409 y:46
			OperatableStateMachine.add('Wonderland_get_waypoint_from_id',
										self.use_behavior(Wonderland_get_waypoint_from_idSM, 'Wonderland_get_waypoint_from_id'),
										transitions={'finished': 'waypoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint_id': 'name', 'json_text': 'json_text'})

			# x:748 y:182
			OperatableStateMachine.add('Move to object',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:721 y:74
			OperatableStateMachine.add('waypoint',
										Wonderland_Get_Waypoint(index_function=lambda x: 0),
										transitions={'done': 'Move to object', 'no_waypoint': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_waypoint': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'index', 'id': 'id', 'name': 'name', 'x': 'x', 'y': 'y', 'theta': 'theta', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
