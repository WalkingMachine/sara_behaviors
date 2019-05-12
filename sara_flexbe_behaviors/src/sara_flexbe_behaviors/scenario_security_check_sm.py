#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_sound import SaraSound
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_pass_door_sm import Action_Pass_DoorSM as sara_flexbe_behaviors__Action_Pass_DoorSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 12 mai 2018
@author: Veronica Romero
'''
class Scenario_Security_CheckSM(Behavior):
	'''
	englobe le scenario du test de securite.
	'''


	def __init__(self):
		super(Scenario_Security_CheckSM, self).__init__()
		self.name = 'Scenario_Security_Check'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Move to test zone')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door')
		self.add_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:358 y:506
		_state_machine = OperatableStateMachine(outcomes=['finished'])
		_state_machine.userdata.relative = False
		_state_machine.userdata.EntryName = "door1/enter"
		_state_machine.userdata.container = None
		_state_machine.userdata.TestName = "Dining Room"
		_state_machine.userdata.ExitName = "door2/exit"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:52 y:27
			OperatableStateMachine.add('Bouton to start',
										ContinueButton(),
										transitions={'true': 'Action_Pass_Door', 'false': 'Bouton to start'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:41 y:430
			OperatableStateMachine.add('Failed',
										SaraSound(sound="error.wav"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:328 y:370
			OperatableStateMachine.add('Waiting',
										SaraSound(sound="to_be_continued.wav"),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:310 y:111
			OperatableStateMachine.add('Move to test zone',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Move to test zone'),
										transitions={'finished': 'say ready', 'failed': 'Failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'TestName'})

			# x:329 y:197
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for my safety check. Press the continue button on my back when you are done.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:34 y:115
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door'),
										transitions={'Done': 'Move to test zone', 'Fail': 'Failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'EntryName'})

			# x:332 y:282
			OperatableStateMachine.add('Bouton continuer',
										ContinueButton(),
										transitions={'true': 'say bye', 'false': 'Waiting'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:513 y:432
			OperatableStateMachine.add('Action_Pass_Door_2',
										self.use_behavior(sara_flexbe_behaviors__Action_Pass_DoorSM, 'Action_Pass_Door_2'),
										transitions={'Done': 'finished', 'Fail': 'Failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorName': 'ExitName'})

			# x:530 y:282
			OperatableStateMachine.add('say bye',
										SaraSay(sentence="Thank you, See you later.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'Action_Pass_Door_2'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
