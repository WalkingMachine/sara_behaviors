#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_find_person')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetKey import SetKey
from behavior_action_find.action_find_sm import Action_findSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.log_key_state import LogKeyState
from behavior_action_turn.action_turn_sm import action_turnSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 30/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_Find_PersonSM(Behavior):
	'''
	Action Wrapper for find a person visually arround the robot.
	'''


	def __init__(self):
		super(ActionWrapper_Find_PersonSM, self).__init__()
		self.name = 'ActionWrapper_Find_Person'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_findSM, 'Action_find')
		self.add_behavior(action_turnSM, 'action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1498 67 
		# Find|n1- what to find|n2- where to look for



	def create(self):
		# x:1399 y:61, x:265 y:777, x:1004 y:649
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["FindPerson","Rachel"]
		_state_machine.userdata.rotation = -1.57

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:55 y:588, x:354 y:578, x:383 y:108
		_sm_ask_confirmation_0 = OperatableStateMachine(outcomes=['yes', 'no', 'error'], input_keys=['name'])

		with _sm_ask_confirmation_0:
			# x:45 y:101
			OperatableStateMachine.add('Repeat the question',
										ForLoop(repeat=5),
										transitions={'do': 'Ask Person', 'end': 'error'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:35 y:303
			OperatableStateMachine.add('Get Yes or No',
										GetSpeech(watchdog=5),
										transitions={'done': 'Repeat', 'nothing': 'Say Not understand', 'fail': 'Say Not understand'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:34 y:486
			OperatableStateMachine.add('Check Yes',
										CheckConditionState(predicate=lambda x: "yes" in x),
										transitions={'true': 'yes', 'false': 'Check No'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})

			# x:310 y:278
			OperatableStateMachine.add('Say Not understand',
										SaraSayKey(Format=lambda x: "I did not understand.", emotion=1, block=True),
										transitions={'done': 'Repeat the question'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:44 y:211
			OperatableStateMachine.add('Ask Person',
										SaraSayKey(Format=lambda x: "Are you " + x + "?", emotion=1, block=True),
										transitions={'done': 'Get Yes or No'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:281 y:476
			OperatableStateMachine.add('Check No',
										CheckConditionState(predicate=lambda x: "no" in x),
										transitions={'true': 'no', 'false': 'Say Not understand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})

			# x:55 y:390
			OperatableStateMachine.add('Repeat',
										LogKeyState(text="I heard: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Check Yes'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'words'})


		# x:305 y:322, x:287 y:53
		_sm_init_1 = OperatableStateMachine(outcomes=['done', 'no_param'], input_keys=['Action'], output_keys=['person', 'name'])

		with _sm_init_1:
			# x:30 y:40
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] is not None and x[1] != ''),
										transitions={'true': 'ReadParameters', 'false': 'no_param'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:102 y:221
			OperatableStateMachine.add('say find object',
										SaraSayKey(Format=lambda x: "I'm now looking for " + x, emotion=1, block=True),
										transitions={'done': 'set person'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:95 y:129
			OperatableStateMachine.add('ReadParameters',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'say find object'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:122 y:297
			OperatableStateMachine.add('set person',
										SetKey(Value="person"),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'person'})



		with _state_machine:
			# x:67 y:70
			OperatableStateMachine.add('Init',
										_sm_init_1,
										transitions={'done': 'Action_find', 'no_param': 'say no object given'},
										autonomy={'done': Autonomy.Inherit, 'no_param': Autonomy.Inherit},
										remapping={'Action': 'Action', 'person': 'person', 'name': 'name'})

			# x:270 y:71
			OperatableStateMachine.add('Action_find',
										self.use_behavior(Action_findSM, 'Action_find'),
										transitions={'done': 'Ask Confirmation', 'pas_done': 'reset Head'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'person', 'entity': 'entity'})

			# x:401 y:658
			OperatableStateMachine.add('Do not find person',
										SaraSay(sentence="I did not find a person.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:918 y:47
			OperatableStateMachine.add('Say found',
										SaraSayKey(Format=lambda x: "I have found " + x + "!", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:596 y:24
			OperatableStateMachine.add('Ask Confirmation',
										_sm_ask_confirmation_0,
										transitions={'yes': 'Say found', 'no': 'Retry', 'error': 'reset Head'},
										autonomy={'yes': Autonomy.Inherit, 'no': Autonomy.Inherit, 'error': Autonomy.Inherit},
										remapping={'name': 'name'})

			# x:642 y:221
			OperatableStateMachine.add('Retry',
										ForLoop(repeat=1),
										transitions={'do': 'Try again', 'end': 'reset Head'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:389 y:341
			OperatableStateMachine.add('Try again',
										SaraSay(sentence="Oh, I will try again.", emotion=1, block=True),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})

			# x:324 y:491
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'Action_find', 'failed': 'reset Head'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:1337 y:389
			OperatableStateMachine.add('reset Head',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Do not find person'},
										autonomy={'done': Autonomy.Off})

			# x:47 y:654
			OperatableStateMachine.add('say no object given',
										SaraSay(sentence="You didn't told me what to find.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
