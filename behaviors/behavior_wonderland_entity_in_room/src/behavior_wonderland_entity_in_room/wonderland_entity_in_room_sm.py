#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_entity_in_room')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_entity.wonderland_get_entity_sm import Wonderland_Get_EntitySM
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Lucas Maurice
'''
class Wonderland_Entity_In_RoomSM(Behavior):
	'''
	List all entities in a specified room.
	'''


	def __init__(self):
		super(Wonderland_Entity_In_RoomSM, self).__init__()
		self.name = 'Wonderland_Entity_In_Room'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:458 y:16, x:299 y:325
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name', 'index'])
		_state_machine.userdata.name = "Table"
		_state_machine.userdata.index = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:80 y:109
			OperatableStateMachine.add('Wonderland_Get_Entity',
										self.use_behavior(Wonderland_Get_EntitySM, 'Wonderland_Get_Entity'),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'entity': 'json_text'})

			# x:426 y:208
			OperatableStateMachine.add('Empty Log',
										LogState(text="There is no entity !", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:548 y:260
			OperatableStateMachine.add('Log',
										LogState(text="Empty 2", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
