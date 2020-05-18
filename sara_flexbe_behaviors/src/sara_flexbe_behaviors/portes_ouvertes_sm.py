#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.actionwrapper_pick_sm import ActionWrapper_PickSM
from sara_flexbe_behaviors.action_opencupboard_sm import Action_OpenCupboardSM
from sara_flexbe_behaviors.actionwrapper_move_sm import ActionWrapper_MoveSM
from sara_flexbe_behaviors.actionwrapper_place_sm import ActionWrapper_PlaceSM
from sara_flexbe_states.run_trajectory import RunTrajectory
from flexbe_states.wait_state import WaitState
from sara_flexbe_behaviors.action_turn_sm import action_turnSM
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
		self.add_behavior(Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick')
		self.add_behavior(Action_OpenCupboardSM, 'Action_OpenCupboard')
		self.add_behavior(ActionWrapper_MoveSM, 'Action_MovePeople')
		self.add_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place')
		self.add_behavior(action_turnSM, 'action_turn')
		self.add_behavior(ActionWrapper_MoveSM, 'Action_MoveTable')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1070 y:493, x:687 y:155
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.MoveToPeople = ["move","crowd"]
		_state_machine.userdata.CupboardName = "cupboard"
		_state_machine.userdata.MoveToTable = ["move","table"]
		_state_machine.userdata.PickObject = ["pick", "bottle"]
		_state_machine.userdata.PlaceObject = ["place", "table"]
		_state_machine.userdata.rotation = 1.5

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_salute_people_0 = OperatableStateMachine(outcomes=['done'])

		with _sm_salute_people_0:
			# x:105 y:52
			OperatableStateMachine.add('wave',
										RunTrajectory(file="Wave", duration=0),
										transitions={'done': 'hi'},
										autonomy={'done': Autonomy.Off})

			# x:95 y:152
			OperatableStateMachine.add('hi',
										SaraSay(sentence="Hi i will show you how great i am.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:107 y:335
			OperatableStateMachine.add('say pick',
										SaraSay(sentence="I will take the bottle from this cupboard and place it on the table.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:116 y:243
			OperatableStateMachine.add('w1',
										WaitState(wait_time=1),
										transitions={'done': 'say pick'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:70 y:37
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'Action_MovePeople', 'failed': 'Action_MovePeople'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:975 y:587
			OperatableStateMachine.add('bye',
										SaraSay(sentence="I am done for the day. Thank you for visiting me!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Init_Sequence'},
										autonomy={'done': Autonomy.Off})

			# x:48 y:551
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick'),
										transitions={'finished': 'Action_MoveTable', 'failed': 'try', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'PickObject'})

			# x:58 y:343
			OperatableStateMachine.add('Action_OpenCupboard',
										self.use_behavior(Action_OpenCupboardSM, 'Action_OpenCupboard'),
										transitions={'finished': 'say looking', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'CupboardName'})

			# x:60 y:653
			OperatableStateMachine.add('try',
										SaraSay(sentence="I will try again", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Action_OpenCupboard'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:152
			OperatableStateMachine.add('Action_MovePeople',
										self.use_behavior(ActionWrapper_MoveSM, 'Action_MovePeople'),
										transitions={'finished': 'Salute people', 'failed': 'Action_MovePeople', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToPeople'})

			# x:621 y:485
			OperatableStateMachine.add('ActionWrapper_Place',
										self.use_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place'),
										transitions={'finished': 'wave', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'PlaceObject'})

			# x:75 y:247
			OperatableStateMachine.add('Salute people',
										_sm_salute_people_0,
										transitions={'done': 'Action_OpenCupboard'},
										autonomy={'done': Autonomy.Inherit})

			# x:772 y:588
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'bye', 'failed': 'bye'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:349 y:485
			OperatableStateMachine.add('Action_MoveTable',
										self.use_behavior(ActionWrapper_MoveSM, 'Action_MoveTable'),
										transitions={'finished': 'ActionWrapper_Place', 'failed': 'Action_MoveTable', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'MoveToTable'})

			# x:70 y:445
			OperatableStateMachine.add('say looking',
										SaraSay(sentence="I'm now looking for the bottle.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'ActionWrapper_Pick'},
										autonomy={'done': Autonomy.Off})

			# x:833 y:462
			OperatableStateMachine.add('wave',
										RunTrajectory(file="Wave", duration=0),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
