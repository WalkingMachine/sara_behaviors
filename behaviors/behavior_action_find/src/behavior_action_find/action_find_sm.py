#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_find')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.wait_state import WaitState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from behavior_action_turn.action_turn_sm import action_turnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Lucas Maurice
'''
class Action_findSM(Behavior):
	'''
	Find an entity arround sara, identified by entity class.
	'''


	def __init__(self):
		super(Action_findSM, self).__init__()
		self.name = 'Action_find'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Container/Rotation/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1068 y:92, x:998 y:309
		_state_machine = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'])
		_state_machine.userdata.className = "person"
		_state_machine.userdata.entity = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:854 y:150
		_sm_rotation_0 = OperatableStateMachine(outcomes=['end'])

		with _sm_rotation_0:
			# x:191 y:89
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:419 y:97
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Container/Rotation/action_turn'),
										transitions={'finished': 'end', 'failed': 'end'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})


		# x:683 y:188, x:473 y:345
		_sm_find_entity_1 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'])

		with _sm_find_entity_1:
			# x:181 y:178
			OperatableStateMachine.add('find_entity',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'Get Entity', 'not_found': 'WaitState'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'className', 'list_entities_by_name': 'list_entities_by_name', 'number': 'number'})

			# x:194 y:40
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'find_entity'},
										autonomy={'done': Autonomy.Off})

			# x:454 y:178
			OperatableStateMachine.add('Get Entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'list_entities_by_name', 'output_value': 'entity'})


		# x:372 y:27, x:370 y:220, x:368 y:100, x:330 y:458, x:460 y:465
		_sm_container_2 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'], conditions=[
										('not_found', [('Rotation', 'end')]),
										('found', [('Find Entity', 'found')]),
										('not_found', [('Find Entity', 'not_found')])
										])

		with _sm_container_2:
			# x:131 y:44
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_1,
										transitions={'found': 'found', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:129 y:197
			OperatableStateMachine.add('Rotation',
										_sm_rotation_0,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit})



		with _state_machine:
			# x:465 y:137
			OperatableStateMachine.add('Container',
										_sm_container_2,
										transitions={'found': 'found', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
