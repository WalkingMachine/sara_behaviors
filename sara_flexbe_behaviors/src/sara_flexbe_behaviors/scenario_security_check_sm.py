#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_sound import SaraSound
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_pass_door.action_pass_door_sm import Action_Pass_DoorSM
from sara_flexbe_states.WonderlandGetEntityVerbal import WonderlandGetEntityVerbal
from flexbe_states.calculation_state import CalculationState
from flexbe_states.log_key_state import LogKeyState
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
		self.add_behavior(Action_MoveSM, 'Move to test zone')
		self.add_behavior(Action_Pass_DoorSM, 'Action_Pass_Door')
		self.add_behavior(Action_Pass_DoorSM, 'Action_Pass_Door_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1166 y:631
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
			# x:189 y:9
			OperatableStateMachine.add('Bouton to start',
										ContinueButton(),
										transitions={'true': 'set not relative', 'false': 'Bouton to start'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:37 y:612
			OperatableStateMachine.add('Failed',
										SaraSound(sound="error.wav"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:369 y:551
			OperatableStateMachine.add('Waiting',
										SaraSound(sound="to_be_continued.wav"),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:24 y:498
			OperatableStateMachine.add('Move to test zone',
										self.use_behavior(Action_MoveSM, 'Move to test zone'),
										transitions={'finished': 'say ready', 'failed': 'Failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'TestPose', 'relative': 'relative'})

			# x:226 y:489
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for my safety check. Press the continue button on my back when you are done.", emotion=1, block=True),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:24 y:259
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'Action_Pass_Door'),
										transitions={'Done': 'get test zone', 'Fail': 'Failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'DoorPose1'})

			# x:359 y:480
			OperatableStateMachine.add('Bouton continuer',
										ContinueButton(),
										transitions={'true': 'say bye', 'false': 'Waiting'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:1002 y:463
			OperatableStateMachine.add('Action_Pass_Door_2',
										self.use_behavior(Action_Pass_DoorSM, 'Action_Pass_Door_2'),
										transitions={'Done': 'finished', 'Fail': 'Failed'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'DoorPose2'})

			# x:27 y:104
			OperatableStateMachine.add('get entry',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get waypoint entry', 'multiple': 'get waypoint entry', 'none': 'get waypoint entry', 'error': 'get waypoint entry'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'EntryName', 'containers': 'container', 'entities': 'DoorPose1'})

			# x:39 y:176
			OperatableStateMachine.add('get waypoint entry',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'DoorPose1', 'output_value': 'DoorPose1'})

			# x:25 y:413
			OperatableStateMachine.add('get waypoint test',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'Move to test zone'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'TestPose', 'output_value': 'TestPose'})

			# x:646 y:472
			OperatableStateMachine.add('get exit zone',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get exit pose', 'multiple': 'get exit pose', 'none': 'get exit pose', 'error': 'get exit pose'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'ExitName', 'containers': 'container', 'entities': 'DoorPose2'})

			# x:855 y:470
			OperatableStateMachine.add('get exit pose',
										CalculationState(calculation=lambda x: x.waypoint),
										transitions={'done': 'log'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'DoorPose2', 'output_value': 'DoorPose2'})

			# x:921 y:334
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_Pass_Door_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'DoorPose2'})

			# x:519 y:476
			OperatableStateMachine.add('say bye',
										SaraSay(sentence="Thank you, See you later.", emotion=1, block=True),
										transitions={'done': 'get exit zone'},
										autonomy={'done': Autonomy.Off})

			# x:17 y:335
			OperatableStateMachine.add('get test zone',
										WonderlandGetEntityVerbal(),
										transitions={'one': 'get waypoint test', 'multiple': 'get waypoint test', 'none': 'get waypoint test', 'error': 'get waypoint test'},
										autonomy={'one': Autonomy.Off, 'multiple': Autonomy.Off, 'none': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'name': 'TestName', 'containers': 'container', 'entities': 'TestPose'})

			# x:49 y:34
			OperatableStateMachine.add('set not relative',
										SetKey(Value=False),
										transitions={'done': 'get entry'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
