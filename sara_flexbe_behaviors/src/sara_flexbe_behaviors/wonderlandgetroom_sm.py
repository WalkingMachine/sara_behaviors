#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 05 2019
@author: Alexandre Mongrain
'''
class WonderlandGetRoomSM(Behavior):
	'''
	Returns the top level container ID from the ID of an Entity.
	'''


	def __init__(self):
		super(WonderlandGetRoomSM, self).__init__()
		self.name = 'WonderlandGetRoom'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 332 359 
		# Dépend de ce qui est retourné lorsqu'il ny a pas de container. Si ça fait que wonderland retourne une erreur on pogne le dernierr entity inspecté.



	def create(self):
		# x:42 y:502, x:623 y:168
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['EntityId'], output_keys=['ContainerId'])
		_state_machine.userdata.EntityId = 45
		_state_machine.userdata.ContainerId = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:111 y:46
			OperatableStateMachine.add('GetWonderlandEntity',
										WonderlandGetEntityByID(),
										transitions={'found': 'GetContainer', 'not_found': 'failed', 'error': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'EntityId', 'entity': 'Entity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:257 y:303
			OperatableStateMachine.add('GetWonderlandEntity_2',
										WonderlandGetEntityByID(),
										transitions={'found': 'ClimbALevel', 'not_found': 'ThisIsTheContainer', 'error': 'ThisIsTheContainer'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'ContainerId', 'entity': 'Entity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

			# x:245 y:175
			OperatableStateMachine.add('ClimbALevel',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'GetWonderlandEntity'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'ContainerId', 'output_value': 'EntityId'})

			# x:126 y:432
			OperatableStateMachine.add('ThisIsTheContainer',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'EntityId', 'output_value': 'ContainerId'})

			# x:29 y:172
			OperatableStateMachine.add('GetContainer',
										CalculationState(calculation=lambda x: x.containerId),
										transitions={'done': 'if as container'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'ContainerId'})

			# x:39 y:291
			OperatableStateMachine.add('if as container',
										CheckConditionState(predicate=lambda x: x.containerId),
										transitions={'true': 'GetWonderlandEntity_2', 'false': 'ThisIsTheContainer'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
