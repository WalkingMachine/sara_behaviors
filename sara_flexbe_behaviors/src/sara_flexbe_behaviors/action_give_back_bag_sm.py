#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.torque_reader import ReadTorque
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
		# x:459 y:476, x:402 y:174
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.effort = 0
		_state_machine.userdata.Open_gripper = 255

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:73 y:35
			OperatableStateMachine.add('setTarget',
										SetKey(Value="Help_me_carry"),
										transitions={'done': 'Give_back'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:58 y:216
			OperatableStateMachine.add('Open_gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'Say_to take_bag', 'no_object': 'Say_to take_bag'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:54 y:315
			OperatableStateMachine.add('Say_to take_bag',
										SaraSay(sentence="Here is your bag. It was a pleasure helping you", input_keys=[], emotion=1, block=True),
										transitions={'done': 'detectObject'},
										autonomy={'done': Autonomy.Off})

			# x:73 y:122
			OperatableStateMachine.add('Give_back',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Open_gripper', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:60 y:404
			OperatableStateMachine.add('detectObject',
										ReadTorque(watchdog=5, Joint="right_elbow_pitch_joint", Threshold=0.1, min_time=2),
										transitions={'threshold': 'Close', 'watchdog': 'Close', 'fail': 'Close'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:39 y:537
			OperatableStateMachine.add('Close',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'Finished', 'no_object': 'Finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:231 y:545
			OperatableStateMachine.add('Finished',
										SaraSay(sentence="It was a pleasure", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
