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
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_behaviors.action_turn_sm import action_turnSM
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 05 2019
@author: Quentin Gaillot
'''
class Action_findPersonByIDSM(Behavior):
	'''
	Find a person with its ID
	'''


	def __init__(self):
		super(Action_findPersonByIDSM, self).__init__()
		self.name = 'Action_findPersonByID'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Container/Rotation/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

	# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:93 y:313, x:514 y:143
		_state_machine = OperatableStateMachine(outcomes=['found', 'not_found'], input_keys=['className', 'personID'], output_keys=['personEntity'])
		_state_machine.userdata.className = "person"
		_state_machine.userdata.personID = 0
		_state_machine.userdata.personEntity = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:707 y:760
		_sm_rotation_0 = OperatableStateMachine(outcomes=['end'], output_keys=['personEntity'])

		with _sm_rotation_0:
			# x:51 y:38
			OperatableStateMachine.add('Set 180 degres',
										SetKey(Value=3.1416),
										transitions={'done': 'set cpt to 0'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})

			# x:613 y:470
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Container/Rotation/action_turn'),
										transitions={'finished': 'check is cpt is 1', 'failed': 'check is cpt is 1'},
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

			# x:59 y:128
			OperatableStateMachine.add('set cpt to 0',
										SetKey(Value=0),
										transitions={'done': 'Look Center'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'cpt'})

			# x:400 y:499
			OperatableStateMachine.add('check is cpt is 1',
										CheckConditionState(predicate=lambda x: x==1),
										transitions={'true': 'set entity to unknown', 'false': 'set cpt to 1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'cpt'})

			# x:414 y:210
			OperatableStateMachine.add('set cpt to 1',
										SetKey(Value=1),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'cpt'})

			# x:605 y:659
			OperatableStateMachine.add('set entity to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'end'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personEntity'})


		# x:683 y:188
		_sm_find_entity_1 = OperatableStateMachine(outcomes=['found'], input_keys=['personID'], output_keys=['personEntity'])

		with _sm_find_entity_1:
			# x:226 y:188
			OperatableStateMachine.add('get person',
										GetEntityByID(),
										transitions={'found': 'found', 'not_found': 'WaitState'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'personID', 'Entity': 'personEntity'})

			# x:194 y:40
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'get person'},
										autonomy={'done': Autonomy.Off})


		# x:372 y:27, x:392 y:217, x:400 y:139, x:330 y:458
		_sm_container_2 = ConcurrencyContainer(outcomes=['found', 'not_found'], input_keys=['className', 'personID'], output_keys=['personEntity'], conditions=[
										('not_found', [('Rotation', 'end')]),
										('found', [('Find Entity', 'found')])
										])

		with _sm_container_2:
			# x:131 y:44
			OperatableStateMachine.add('Find Entity',
										_sm_find_entity_1,
										transitions={'found': 'found'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'personID': 'personID', 'personEntity': 'personEntity'})

			# x:135 y:199
			OperatableStateMachine.add('Rotation',
										_sm_rotation_0,
										transitions={'end': 'not_found'},
										autonomy={'end': Autonomy.Inherit},
										remapping={'personEntity': 'personEntity'})



		with _state_machine:
			# x:67 y:42
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'Container'},
										autonomy={'done': Autonomy.Off})

			# x:278 y:138
			OperatableStateMachine.add('Look Center Not Found',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'not_found'},
										autonomy={'done': Autonomy.Off})

			# x:63 y:126
			OperatableStateMachine.add('Container',
										_sm_container_2,
										transitions={'found': 'WaitState', 'not_found': 'Look Center Not Found'},
										autonomy={'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'className': 'className', 'personID': 'personID', 'personEntity': 'personEntity'})

			# x:67 y:222
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=1),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

# [/MANUAL_FUNC]
