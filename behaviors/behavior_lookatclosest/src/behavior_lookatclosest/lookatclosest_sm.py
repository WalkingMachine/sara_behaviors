#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_lookatclosest')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 16 2018
@author: Philippe La Madeleine
'''
class LookAtClosestSM(Behavior):
	'''
	look at the closest object
	'''


	def __init__(self):
		super(LookAtClosestSM, self).__init__()
		self.name = 'LookAtClosest'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365
		_state_machine = OperatableStateMachine(outcomes=['failed'])
		_state_machine.userdata.ObjectName = "person"
		_state_machine.userdata.ID = 2314

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:49 y:113
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.8, distance_max=10),
										transitions={'found': 'getclosest', 'not_found': 'list'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'ObjectName', 'entity_list': 'entity_list', 'number': 'number'})

			# x:296 y:131
			OperatableStateMachine.add('getclosest',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'keep looking'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:207 y:231
			OperatableStateMachine.add('keep looking',
										KeepLookingAt(),
										transitions={'failed': 'list'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
