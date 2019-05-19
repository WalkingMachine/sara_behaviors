#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.set_gripper_state import SetGripperState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Redouane Laref
'''
class Action_Give_Back_BagSM(Behavior):
	'''
	Behavior of giving back the  back.
	'''


	def __init__(self):
		super(Action_Give_Back_BagSM, self).__init__()
		self.name = 'Action_Give_Back_Bag'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:463 y:361, x:402 y:174
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.effort = 0
		_state_machine.userdata.Open_gripper = 255

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:53 y:30
			OperatableStateMachine.add('place arm',
										RunTrajectory(file="receive_bag", duration=6),
										transitions={'done': 'Open_gripper'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:231
			OperatableStateMachine.add('Say_to take_bag',
										SaraSay(sentence="Here is your bag.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'detectObject'},
										autonomy={'done': Autonomy.Off})

			# x:45 y:321
			OperatableStateMachine.add('detectObject',
										ReadTorque(watchdog=10, Joint="right_elbow_pitch_joint", Threshold=0.5, min_time=2),
										transitions={'threshold': 'Finished', 'watchdog': 'Finished', 'fail': 'Finished'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:220 y:472
			OperatableStateMachine.add('Close',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'place back bag', 'no_object': 'place back bag'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:47 y:466
			OperatableStateMachine.add('Finished',
										SaraSay(sentence="It was a pleasure", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Close'},
										autonomy={'done': Autonomy.Off})

			# x:48 y:116
			OperatableStateMachine.add('Open_gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'Say_to take_bag', 'no_object': 'Say_to take_bag'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:420 y:470
			OperatableStateMachine.add('place back bag',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
