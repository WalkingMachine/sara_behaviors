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
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:84 y:465, x:727 y:360
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['className'], output_keys=['entity'])
		_state_machine.userdata.className = "bottle"
		_state_machine.userdata.entity = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:365
		_sm_look_at_0 = OperatableStateMachine(outcomes=['end'], input_keys=['ID'])

		with _sm_look_at_0:
			# x:75 y:135
			OperatableStateMachine.add('look at',
										KeepLookingAt(),
										transitions={'failed': 'look at'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:798 y:597
		_sm_rotation360_1 = OperatableStateMachine(outcomes=['end'])

		with _sm_rotation360_1:
			# x:42 y:34
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3.1416),
										transitions={'done': 'rotate center'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:610 y:293
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=0.6, yaw=1),
										transitions={'done': 'Rotate Right'},
										autonomy={'done': Autonomy.Off})

			# x:406 y:58
			OperatableStateMachine.add('Rotate Left',
										WaitState(wait_time=5),
										transitions={'done': 'rotate center'},
										autonomy={'done': Autonomy.Off})

			# x:410 y:313
			OperatableStateMachine.add('Rotate Right',
										WaitState(wait_time=5),
										transitions={'done': 'look center 2'},
										autonomy={'done': Autonomy.Off})

			# x:209 y:50
			OperatableStateMachine.add('Look Left',
										SaraSetHeadAngle(pitch=0.6, yaw=-1),
										transitions={'done': 'Rotate Left'},
										autonomy={'done': Autonomy.Off})

			# x:216 y:186
			OperatableStateMachine.add('Rotate Left 2',
										WaitState(wait_time=5),
										transitions={'done': 'Look Left'},
										autonomy={'done': Autonomy.Off})

			# x:630 y:170
			OperatableStateMachine.add('wait 5',
										WaitState(wait_time=5),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})

			# x:603 y:47
			OperatableStateMachine.add('rotate center',
										SaraSetHeadAngle(pitch=0.6, yaw=0),
										transitions={'done': 'wait 5'},
										autonomy={'done': Autonomy.Off})

			# x:208 y:308
			OperatableStateMachine.add('look center 2',
										SaraSetHeadAngle(pitch=0.6, yaw=0),
										transitions={'done': 'Rotate Left 2'},
										autonomy={'done': Autonomy.Off})


		# x:683 y:188
		_sm_find_entity_2 = OperatableStateMachine(outcomes=['found'], input_keys=['className'], output_keys=['entity'])

		with _sm_find_entity_2:
			# x:181 y:178
			OperatableStateMachine.add('find_entity',
										list_entities_by_name(frontality_level=0.5, distance_max=2),
										transitions={'found': 'Get Entity', 'none_found': 'find_entity'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'className', 'entity_list': 'entity_list', 'number': 'number'})

			# x:454 y:178
			OperatableStateMachine.add('Get Entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})


		# x:371 y:306, x:130 y:365, x:230 y:365
		_sm_look_for_2_sec_3 = ConcurrencyContainer(outcomes=['done'], input_keys=['ID'], conditions=[
										('done', [('WaitState 2', 'done')]),
										('done', [('Look at', 'end')])
										])

		with _sm_look_for_2_sec_3:
			# x:84 y:166
			OperatableStateMachine.add('Look at',
										_sm_look_at_0,
										transitions={'end': 'done'},
										autonomy={'end': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:345 y:187
			OperatableStateMachine.add('WaitState 2',
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:372 y:27, x:370 y:220, x:368 y:100, x:352 y:305, x:460 y:465
		_sm_find_entity_while_turning360_4 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['className'], output_keys=['entity'], conditions=[
										('not_found', [('Rotation360', 'end')]),
										('found', [('Find Entity', 'found')]),
										('not_found', [('wait', 'done')])
										])

		with _sm_find_entity_while_turning360_4:
			# x:131 y:44
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_2,
										transitions={'found': 'found'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:129 y:197
			OperatableStateMachine.add('Rotation360',
										_sm_rotation360_1,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit})

			# x:149 y:306
			OperatableStateMachine.add('wait',
										WaitState(wait_time=30),
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:55 y:41
			OperatableStateMachine.add('Look Front Center',
										SaraSetHeadAngle(pitch=0.7, yaw=0),
										transitions={'done': 'Find Entity WHILE Turning360'},
										autonomy={'done': Autonomy.Off})

			# x:345 y:156
			OperatableStateMachine.add('Look Center Not Found',
										SaraSetHeadAngle(pitch=0.7, yaw=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:59 y:376
			OperatableStateMachine.add('Log Entity',
										LogKeyState(text="Found entity: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity'})

			# x:26 y:121
			OperatableStateMachine.add('Find Entity WHILE Turning360',
										_sm_find_entity_while_turning360_4,
										transitions={'found': 'get ID', 'not_found': 'Look Center Not Found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:45 y:290
			OperatableStateMachine.add('look for 2 sec',
										_sm_look_for_2_sec_3,
										transitions={'done': 'Log Entity'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:62 y:211
			OperatableStateMachine.add('get ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'look for 2 sec'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
