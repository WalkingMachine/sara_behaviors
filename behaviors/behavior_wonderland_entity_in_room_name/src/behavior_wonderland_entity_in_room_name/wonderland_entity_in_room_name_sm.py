#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_entity_in_room_name')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from flexbe_states.log_state import LogState
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
from sara_flexbe_states.Wonderland_List_Something import Wonderland_List_Something
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Lucas Maurice
'''
class Wonderland_Entity_In_Room_NameSM(Behavior):
	'''
	List all entities in a specified room.
	'''


	def __init__(self):
		super(Wonderland_Entity_In_Room_NameSM, self).__init__()
		self.name = 'Wonderland_Entity_In_Room_Name'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:784 y:51, x:483 y:263
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['room_name'], output_keys=['ids', 'names'])
		_state_machine.userdata.room_name = 'salon'
		_state_machine.userdata.ids = None
		_state_machine.userdata.names = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:72 y:47
			OperatableStateMachine.add('Generate URL',
										CalculationState(calculation=lambda x: "rooms/?name=" + x),
										transitions={'done': 'Wonderland_Request'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'room_name', 'output_value': 'url'})

			# x:464 y:151
			OperatableStateMachine.add('Empty Log',
										LogState(text="There is no entity !", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:221 y:46
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'List_Entities', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'response'})

			# x:432 y:61
			OperatableStateMachine.add('List_Entities',
										Wonderland_List_Something(),
										transitions={'done': 'finished', 'empty': 'Empty Log', 'error': 'Log'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'response', 'ids': 'ids', 'names': 'names'})

			# x:647 y:126
			OperatableStateMachine.add('Log',
										LogState(text="Error while listing entities.", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
