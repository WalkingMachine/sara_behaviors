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
		# x:838 y:239, x:354 y:258
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['effort', 'Open_gripper'])
		_state_machine.userdata.effort = 0
		_state_machine.userdata.Open_gripper = 255

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:112 y:56
			OperatableStateMachine.add('setTarget',
										SetKey(Value="Help_me_carry"),
										transitions={'done': 'Give_back'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:502 y:155
			OperatableStateMachine.add('Open_gripper',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'Say_to take_bag', 'no_object': 'Say_to take_bag'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:767 y:162
			OperatableStateMachine.add('Say_to take_bag',
										SaraSay(sentence="Here is your bag. It was a pleasure helping you", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:262 y:96
			OperatableStateMachine.add('Give_back',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Open_gripper', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
