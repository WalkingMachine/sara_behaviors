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
from flexbe_states.wait_state import WaitState
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
		_state_machine.userdata.ID = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365
		_sm_keeplookingforatime_0 = ConcurrencyContainer(outcomes=['failed'], input_keys=['ID'], conditions=[
										('failed', [('keep looking', 'failed'), ('wait 3', 'done')])
										])

		with _sm_keeplookingforatime_0:
			# x:210 y:103
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=3),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:37 y:128
			OperatableStateMachine.add('keep looking',
										KeepLookingAt(),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:49 y:113
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.8, distance_max=10),
										transitions={'found': 'getclosest', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'ObjectName', 'entity_list': 'entity_list', 'number': 'number'})

			# x:296 y:131
			OperatableStateMachine.add('getclosest',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'KeepLookingForATime'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'ID'})

			# x:220 y:258
			OperatableStateMachine.add('KeepLookingForATime',
										_sm_keeplookingforatime_0,
										transitions={'failed': 'list'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
