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
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
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
		self.add_behavior(ActionWrapper_MoveSM, 'Action_MovePeople')
		self.add_behavior(ActionWrapper_MoveSM, 'Action_MoveTable')
		self.add_behavior(ActionWrapper_MoveSM, 'Action_Move_Armoire')
		self.add_behavior(Action_pickSM, 'Action_pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1187 y:429, x:490 y:43
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.MoveToPeople = ["move","waypointpeople"]
		_state_machine.userdata.MoveToArmoire = ["move","waypointarmoire"]
		_state_machine.userdata.MoveToTable = ["move","waypointtable"]
		_state_machine.userdata.objectID = objetID

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:314 y:367, x:230 y:365
		_sm_open_door_0 = OperatableStateMachine(outcomes=['fail', 'door open'], output_keys=['fail', 'done'])

		with _sm_open_door_0:
			# x:139 y:139
			OperatableStateMachine.add('dooropen',
										DoorDetector(timeout=3),
										transitions={'done': 'door open', 'failed': 'door'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:381 y:201
			OperatableStateMachine.add('door',
										RunTrajectory(file="OuvrePorte3"),
										transitions={'done': 'door open'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:27 y:42
			OperatableStateMachine.add('Action_MovePeople',
										self.use_behavior(ActionWrapper_MoveSM, 'Action_MovePeople'),
										transitions={'finished': 'hi', 'failed': 'Action_MovePeople', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToPeople'})

			# x:617 y:170
			OperatableStateMachine.add('Action_MoveTable',
										self.use_behavior(ActionWrapper_MoveSM, 'Action_MoveTable'),
										transitions={'finished': 'releaseobject', 'failed': 'Action_MoveTable', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToTable'})

			# x:107 y:191
			OperatableStateMachine.add('Action_Move_Armoire',
										self.use_behavior(ActionWrapper_MoveSM, 'Action_Move_Armoire'),
										transitions={'finished': 'Open Door', 'failed': 'Action_Move_Armoire', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToArmoire'})

			# x:248 y:273
			OperatableStateMachine.add('Open Door',
										_sm_open_door_0,
										transitions={'fail': 'failed', 'door open': 'Action_pick'},
										autonomy={'fail': Autonomy.Inherit, 'door open': Autonomy.Inherit},
										remapping={'fail': 'fail', 'done': 'done'})

			# x:989 y:331
			OperatableStateMachine.add('bye',
										SaraSay(sentence="I am done for the day", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:423 y:259
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'Action_MoveTable', 'unreachable': 'try', 'not found': 'notfound', 'dropped': 'Action_pick'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'objectID'})

			# x:310 y:376
			OperatableStateMachine.add('try',
										SaraSay(sentence="I will try again", emotion=1, block=True),
										transitions={'done': 'Action_pick'},
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
										transitions={'done': 'Action_Move_Armoire'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
