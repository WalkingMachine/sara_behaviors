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
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.torque_reader import ReadTorque
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 16 2019
@author: Quentin Gaillot
'''
class Action_TakeBagSM(Behavior):
	'''
	Take bag pour le scenarion take out the garbage
	'''


	def __init__(self):
		super(Action_TakeBagSM, self).__init__()
		self.name = 'Action_TakeBag'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:956 y:423, x:999 y:62
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_torque_control_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_torque_control_0:
			# x:126 y:51
			OperatableStateMachine.add('w2',
										WaitState(wait_time=2),
										transitions={'done': 'check torque'},
										autonomy={'done': Autonomy.Off})

			# x:120 y:195
			OperatableStateMachine.add('check torque',
										ReadTorque(watchdog=20, Joint="right_shoulder_pitch_joint", Threshold=2, min_time=0.5),
										transitions={'threshold': 'finished', 'watchdog': 'check torque', 'fail': 'check torque'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})


		# x:30 y:458, x:130 y:458
		_sm_trajectory_down_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_trajectory_down_1:
			# x:68 y:158
			OperatableStateMachine.add('run down',
										RunTrajectory(file="poubelle_app", duration=20),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:479 y:236, x:469 y:51, x:462 y:111, x:471 y:160, x:430 y:365, x:530 y:365
		_sm_trajectory_down_with_torque_limit_2 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('torque control', 'finished')]),
										('finished', [('trajectory down', 'finished')]),
										('failed', [('trajectory down', 'failed')]),
										('failed', [('torque control', 'failed')])
										])

		with _sm_trajectory_down_with_torque_limit_2:
			# x:109 y:63
			OperatableStateMachine.add('trajectory down',
										_sm_trajectory_down_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:102 y:211
			OperatableStateMachine.add('torque control',
										_sm_torque_control_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		# x:30 y:458, x:130 y:458
		_sm_has_bag_in_gripper_3 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_has_bag_in_gripper_3:
			# x:48 y:101
			OperatableStateMachine.add('say',
										SaraSay(sentence="I must check if I have a bag in my gripper.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_trajectory_up_4 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_trajectory_up_4:
			# x:71 y:122
			OperatableStateMachine.add('trajectory up',
										RunTrajectory(file="poubelle_eloigne", duration=8),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458
		_sm_close_gripper_5 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_close_gripper_5:
			# x:79 y:177
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'finished', 'no_object': 'retry close'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:272 y:237
			OperatableStateMachine.add('retry close',
										ForLoop(repeat=1),
										transitions={'do': 'close gripper', 'end': 'failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})



		with _state_machine:
			# x:89 y:35
			OperatableStateMachine.add('head down',
										SaraSetHeadAngle(pitch=0.8, yaw=0),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:484 y:164
			OperatableStateMachine.add('close gripper',
										_sm_close_gripper_5,
										transitions={'finished': 'trajectory up', 'failed': 'trajectory up'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:473 y:300
			OperatableStateMachine.add('trajectory up',
										_sm_trajectory_up_4,
										transitions={'finished': 'has bag in gripper', 'failed': 'has bag in gripper'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:232 y:434
			OperatableStateMachine.add('has bag in gripper',
										_sm_has_bag_in_gripper_3,
										transitions={'finished': 'finished', 'failed': 'open gripper'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:467 y:33
			OperatableStateMachine.add('trajectory down with torque limit',
										_sm_trajectory_down_with_torque_limit_2,
										transitions={'finished': 'close gripper', 'failed': 'head down'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:283 y:83
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.12, effort=0),
										transitions={'object': 'trajectory down with torque limit', 'no_object': 'trajectory down with torque limit'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
