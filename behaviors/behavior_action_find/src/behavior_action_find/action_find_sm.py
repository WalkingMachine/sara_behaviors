#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_find')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.wait_state import WaitState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from behavior_action_turn.action_turn_sm import action_turnSM
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Lucas Maurice
'''
class Action_findSM(Behavior):
	'''
	Find an entity around sara (will only rotate, won't move), identified by entity class.
	'''


	def __init__(self):
		super(Action_findSM, self).__init__()
		self.name = 'Action_find'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Find Entity WHILE Turning360/Rotation360/action_turn')
		self.add_behavior(action_look_at_faceSM, 'action_look_at_face')
		self.add_behavior(action_look_at_faceSM, 'action_look_at_face_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1038 y:503, x:727 y:360
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['className'], output_keys=['entity'])
		_state_machine.userdata.className = "bottle"
		_state_machine.userdata.entity = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:422 y:153
		_sm_rotation360_0 = OperatableStateMachine(outcomes=['end'])

		with _sm_rotation360_0:
			# x:83 y:39
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3.1416),
										transitions={'done': 'Look Left'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:837 y:101
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Find Entity WHILE Turning360/Rotation360/action_turn'),
										transitions={'finished': 'Look Right 2', 'failed': 'end'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:421 y:54
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=0.7, yaw=-1),
										transitions={'done': 'Rotate Right'},
										autonomy={'done': Autonomy.Off})

			# x:265 y:56
			OperatableStateMachine.add('Rotate Left',
										WaitState(wait_time=8),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})

			# x:630 y:56
			OperatableStateMachine.add('Rotate Right',
										WaitState(wait_time=12),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})

			# x:77 y:128
			OperatableStateMachine.add('Look Left',
										SaraSetHeadAngle(pitch=0.7, yaw=1),
										transitions={'done': 'Rotate Left'},
										autonomy={'done': Autonomy.Off})

			# x:426 y:240
			OperatableStateMachine.add('Look Left 2',
										SaraSetHeadAngle(pitch=0.7, yaw=1),
										transitions={'done': 'Rotate Left 2'},
										autonomy={'done': Autonomy.Off})

			# x:805 y:226
			OperatableStateMachine.add('Look Right 2',
										SaraSetHeadAngle(pitch=0.7, yaw=-1),
										transitions={'done': 'Rotate Right 2'},
										autonomy={'done': Autonomy.Off})

			# x:152 y:234
			OperatableStateMachine.add('Rotate Left 2',
										WaitState(wait_time=12),
										transitions={'done': 'end'},
										autonomy={'done': Autonomy.Off})

			# x:637 y:231
			OperatableStateMachine.add('Rotate Right 2',
										WaitState(wait_time=8),
										transitions={'done': 'Look Left 2'},
										autonomy={'done': Autonomy.Off})


		# x:683 y:188, x:473 y:345
		_sm_find_entity_1 = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'])

		with _sm_find_entity_1:
			# x:181 y:178
			OperatableStateMachine.add('find_entity',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'Get Entity', 'not_found': 'WaitState'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

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
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})


		# x:372 y:27, x:370 y:220, x:368 y:100, x:330 y:458, x:460 y:465
		_sm_find_entity_while_turning360_2 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'], conditions=[
										('not_found', [('Rotation360', 'end')]),
										('found', [('Find Entity', 'found')]),
										('not_found', [('Find Entity', 'not_found')])
										])

		with _sm_find_entity_while_turning360_2:
			# x:131 y:44
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_1,
										transitions={'found': 'found', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:129 y:197
			OperatableStateMachine.add('Rotation360',
										_sm_rotation360_0,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit})



		with _state_machine:
			# x:148 y:101
			OperatableStateMachine.add('Look Front Center',
										SaraSetHeadAngle(pitch=0.5, yaw=0),
										transitions={'done': 'Find Entity WHILE Turning360'},
										autonomy={'done': Autonomy.Off})

			# x:574 y:63
			OperatableStateMachine.add('Look Center Found',
										SaraSetHeadAngle(pitch=0.5, yaw=0),
										transitions={'done': 'Log Entity'},
										autonomy={'done': Autonomy.Off})

			# x:573 y:223
			OperatableStateMachine.add('Look Center Not Found',
										SaraSetHeadAngle(pitch=0.5, yaw=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:773 y:38
			OperatableStateMachine.add('Log Entity',
										LogKeyState(text="Found entity: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'action_look_at_face'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity'})

			# x:338 y:107
			OperatableStateMachine.add('Find Entity WHILE Turning360',
										_sm_find_entity_while_turning360_2,
										transitions={'found': 'WaitState', 'not_found': 'Look Center Not Found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:635 y:153
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'Look Center Found'},
										autonomy={'done': Autonomy.Off})

			# x:969 y:53
			OperatableStateMachine.add('action_look_at_face',
										self.use_behavior(action_look_at_faceSM, 'action_look_at_face'),
										transitions={'finished': 'WaitState 1', 'failed': 'WaitState 1'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'entity'})

			# x:1024 y:197
			OperatableStateMachine.add('WaitState 1',
										WaitState(wait_time=2),
										transitions={'done': 'action_look_at_face_2'},
										autonomy={'done': Autonomy.Off})

			# x:983 y:357
			OperatableStateMachine.add('action_look_at_face_2',
										self.use_behavior(action_look_at_faceSM, 'action_look_at_face_2'),
										transitions={'finished': 'done', 'failed': 'done'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
