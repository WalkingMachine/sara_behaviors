#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as sara_flexbe_behaviors__action_turnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Lucas Maurice
'''
class Action_findPersonSM(Behavior):
	'''
	Find an entity arround sara, identified by entity class.
	'''


	def __init__(self):
		super(Action_findPersonSM, self).__init__()
		self.name = 'Action_findPerson'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'Container/Rotation/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:72 y:443, x:514 y:143
		_state_machine = OperatableStateMachine(outcomes=['done', 'pas_done'], input_keys=['className'], output_keys=['entity'])
		_state_machine.userdata.className = "person"
		_state_machine.userdata.entity = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:706 y:647
		_sm_rotation_0 = OperatableStateMachine(outcomes=['end'])

		with _sm_rotation_0:
			# x:51 y:38
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3.1416),
										transitions={'done': 'Look Center'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:613 y:470
			OperatableStateMachine.add('action_turn',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'Container/Rotation/action_turn'),
										transitions={'finished': 'Look Right', 'failed': 'Look Right'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:421 y:54
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:265 y:56
			OperatableStateMachine.add('w1',
										WaitState(wait_time=4),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})

			# x:630 y:56
			OperatableStateMachine.add('w2',
										WaitState(wait_time=4),
										transitions={'done': 'center'},
										autonomy={'done': Autonomy.Off})

			# x:250 y:177
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:618 y:304
			OperatableStateMachine.add('Look Left 2',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'w4'},
										autonomy={'done': Autonomy.Off})

			# x:612 y:138
			OperatableStateMachine.add('center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:635 y:214
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'Look Left 2'},
										autonomy={'done': Autonomy.Off})

			# x:636 y:394
			OperatableStateMachine.add('w4',
										WaitState(wait_time=4),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})


		# x:683 y:188
		_sm_find_entity_1 = OperatableStateMachine(outcomes=['found'], input_keys=['className'], output_keys=['entity'])

		with _sm_find_entity_1:
			# x:181 y:178
			OperatableStateMachine.add('find_entity',
										list_entities_by_name(frontality_level=0.5, distance_max=4),
										transitions={'found': 'Get Entity', 'none_found': 'find_entity'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:454 y:178
			OperatableStateMachine.add('Get Entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})

			# x:194 y:40
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'find_entity'},
										autonomy={'done': Autonomy.Off})


		# x:372 y:27, x:370 y:220, x:368 y:100, x:330 y:458
		_sm_container_2 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'], conditions=[
										('not_found', [('Rotation', 'end')]),
										('found', [('Find Entity', 'found')])
										])

		with _sm_container_2:
			# x:131 y:44
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_1,
										transitions={'found': 'found'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:129 y:197
			OperatableStateMachine.add('Rotation',
										_sm_rotation_0,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit})



		with _state_machine:
			# x:67 y:42
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'Container'},
										autonomy={'done': Autonomy.Off})

			# x:278 y:138
			OperatableStateMachine.add('Look Center Not Found',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'pas_done'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:326
			OperatableStateMachine.add('Log Entity',
										LogKeyState(text="Found entity: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity'})

			# x:63 y:126
			OperatableStateMachine.add('Container',
										_sm_container_2,
										transitions={'found': 'WaitState', 'not_found': 'Look Center Not Found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:67 y:222
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'Log Entity'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
