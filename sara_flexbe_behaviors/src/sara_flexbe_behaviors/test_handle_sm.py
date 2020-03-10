#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.talker import handleBag
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Mar 07 2020
@author: ayoub 
'''
class test_handleSM(Behavior):
	'''
	test
	'''


	def __init__(self):
		super(test_handleSM, self).__init__()
		self.name = 'test_handle'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:697 y:281, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = 45

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:58 y:136
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'first', 'none_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:338 y:74
			OperatableStateMachine.add('first',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'had'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'output_value'})

			# x:472 y:179
			OperatableStateMachine.add('had',
										handleBag(),
										transitions={'does_have_handle': 'finished', 'does_not_have_handle': 'failed'},
										autonomy={'does_have_handle': Autonomy.Off, 'does_not_have_handle': Autonomy.Off},
										remapping={'entity': 'output_value'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
