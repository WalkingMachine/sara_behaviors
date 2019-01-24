#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.actionwrapper_move_sm import ActionWrapper_MoveSM as sara_flexbe_behaviors__ActionWrapper_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_behaviors.actionwrapper_pick_sm import ActionWrapper_PickSM as sara_flexbe_behaviors__ActionWrapper_PickSM
from sara_flexbe_behaviors.action_opencupboard_sm import Action_OpenCupboardSM as sara_flexbe_behaviors__Action_OpenCupboardSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jan 22 2019
@author: Huynh-Anh et Philippe
'''
class Portes_ouvertesSM(Behavior):
	'''
	sequence qui permet de prendre un objet dans une armoire et la placer sur une table
	'''


	def __init__(self):
		super(Portes_ouvertesSM, self).__init__()
		self.name = 'Portes_ouvertes'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'Action_MovePeople')
		self.add_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'Action_MoveTable')
		self.add_behavior(sara_flexbe_behaviors__ActionWrapper_PickSM, 'ActionWrapper_Pick')
		self.add_behavior(sara_flexbe_behaviors__Action_OpenCupboardSM, 'Action_OpenCupboard')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1187 y:429, x:490 y:43
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.MoveToPeople = ["move","crowd"]
		_state_machine.userdata.CupboardName = "cupboard"
		_state_machine.userdata.MoveToTable = ["move","table"]
		_state_machine.userdata.PickObject = ["pick", "bottle"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:27 y:42
			OperatableStateMachine.add('Action_MovePeople',
										self.use_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'Action_MovePeople'),
										transitions={'finished': 'hi', 'failed': 'Action_MovePeople', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToPeople'})

			# x:617 y:170
			OperatableStateMachine.add('Action_MoveTable',
										self.use_behavior(sara_flexbe_behaviors__ActionWrapper_MoveSM, 'Action_MoveTable'),
										transitions={'finished': 'releaseobject', 'failed': 'Action_MoveTable', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToTable'})

			# x:989 y:331
			OperatableStateMachine.add('bye',
										SaraSay(sentence="I am done for the day", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:630 y:323
			OperatableStateMachine.add('notfound',
										SaraSay(sentence="I can not find it", emotion=1, block=True),
										transitions={'done': 'Action_MoveTable'},
										autonomy={'done': Autonomy.Off})

			# x:838 y:247
			OperatableStateMachine.add('releaseobject',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'bye', 'no_object': 'bye'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:85 y:122
			OperatableStateMachine.add('hi',
										SaraSay(sentence="Hi i will show you how great i am", emotion=1, block=True),
										transitions={'done': 'Action_OpenCupboard'},
										autonomy={'done': Autonomy.Off})

			# x:423 y:515
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(sara_flexbe_behaviors__ActionWrapper_PickSM, 'ActionWrapper_Pick'),
										transitions={'finished': 'notfound', 'failed': 'try', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'PickObject'})

			# x:156 y:279
			OperatableStateMachine.add('Action_OpenCupboard',
										self.use_behavior(sara_flexbe_behaviors__Action_OpenCupboardSM, 'Action_OpenCupboard'),
										transitions={'finished': 'ActionWrapper_Pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'CupboardName'})

			# x:199 y:497
			OperatableStateMachine.add('try',
										SaraSay(sentence="I will try again", emotion=1, block=True),
										transitions={'done': 'ActionWrapper_Pick'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
