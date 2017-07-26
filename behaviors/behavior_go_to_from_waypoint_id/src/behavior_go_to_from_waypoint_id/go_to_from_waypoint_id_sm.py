#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_go_to_from_waypoint_id')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_waypoint_from_id.wonderland_get_waypoint_from_id_sm import Wonderland_get_waypoint_from_idSM
from sara_flexbe_states.Wonderland_Get_Waypoint import Wonderland_Get_Waypoint
from sara_flexbe_states.sara_move_base import SaraMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 26 2017
@author: Redouane Laref
'''
class Go_To_From_Waypoint_IDSM(Behavior):
	'''
	Going to a positionf by  waypoint from it's ID.
	'''


	def __init__(self):
		super(Go_To_From_Waypoint_IDSM, self).__init__()
		self.name = 'Go_To_From_Waypoint_ID'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_get_waypoint_from_idSM, 'Wonderland_get_waypoint_from_id')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:818 y:285, x:392 y:323
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['waypoint_id'])
		_state_machine.userdata.waypoint_id = ""
		_state_machine.userdata.json_text = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:135 y:125
			OperatableStateMachine.add('Wonderland_get_waypoint_from_id',
										self.use_behavior(Wonderland_get_waypoint_from_idSM, 'Wonderland_get_waypoint_from_id'),
										transitions={'finished': 'Waypoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint_id': 'waypoint_id', 'json_text': 'json_text'})

			# x:529 y:113
			OperatableStateMachine.add('Waypoint',
										Wonderland_Get_Waypoint(index_function=lambda x: 0),
										transitions={'done': 'Move', 'no_waypoint': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_waypoint': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'waypoint_id', 'id': 'id', 'name': 'name', 'x': 'x', 'y': 'y', 'theta': 'theta', 'pose': 'pose'})

			# x:848 y:133
			OperatableStateMachine.add('Move',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
