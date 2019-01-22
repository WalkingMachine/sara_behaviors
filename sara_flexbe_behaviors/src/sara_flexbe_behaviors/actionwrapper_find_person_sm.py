#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_find_person')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.for_loop import ForLoop
from behavior_action_turn.action_turn_sm import action_turnSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.SetRosParam import SetRosParam
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.SetKey import SetKey
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
		self.add_behavior(Action_findPersonSM, 'Action_findPerson')
		self.add_behavior(action_turnSM, 'action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1498 67 
		# Find|n1- what to find|n2- where to look for



	def create(self):
		# x:1372 y:392, x:1264 y:482, x:1004 y:649
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["FindPerson","philippe"]
		_state_machine.userdata.rotation = -1.57
		_state_machine.userdata.className = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:458
		_sm_look_at_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['entity'])

		with _sm_look_at_0:
			# x:142 y:112
			OperatableStateMachine.add('get ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'look'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'ID'})

			# x:106 y:262
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'look'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:297 y:737, x:531 y:481, x:378 y:120, x:739 y:299
		_sm_ask_confirmation_1 = OperatableStateMachine(outcomes=['yes', 'no', 'error', 'noname'], input_keys=['name'])

		with _sm_ask_confirmation_1:
			# x:473 y:44
			OperatableStateMachine.add('check if ask name',
										CheckConditionState(predicate=lambda x: x[1] != ""),
										transitions={'true': 'Repeat the question', 'false': 'wait 2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'name'})

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

			# x:529 y:253
			OperatableStateMachine.add('say hi',
										SaraSay(sentence="Hi there", emotion=1, block=True),
										transitions={'done': 'noname'},
										autonomy={'done': Autonomy.Off})

			# x:534 y:159
			OperatableStateMachine.add('wait 2',
										WaitState(wait_time=2),
										transitions={'done': 'say hi'},
										autonomy={'done': Autonomy.Off})

			# x:45 y:101
			OperatableStateMachine.add('Repeat the question',
										ForLoop(repeat=5),
										transitions={'do': 'Ask Person', 'end': 'error'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})


		# x:305 y:322, x:287 y:53
		_sm_if_need_the_one_2 = OperatableStateMachine(outcomes=['done', 'no_param'], input_keys=['Action'], output_keys=['person', 'name'])

		with _sm_if_need_the_one_2:
			# x:30 y:40
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != None and x[1] != ''),
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


		# x:499 y:233, x:499 y:138, x:508 y:57, x:467 y:328, x:430 y:458, x:530 y:458, x:630 y:458, x:470 y:369, x:840 y:558
		_sm_confirm_and_look_at_3 = ConcurrencyContainer(outcomes=['yes', 'no', 'error', 'noname'], input_keys=['name', 'entity'], conditions=[
										('yes', [('Ask Confirmation', 'yes')]),
										('no', [('Ask Confirmation', 'no')]),
										('error', [('Ask Confirmation', 'error')]),
										('noname', [('Ask Confirmation', 'noname')]),
										('error', [('look at', 'finished')])
										])

		with _sm_confirm_and_look_at_3:
			# x:176 y:40
			OperatableStateMachine.add('Ask Confirmation',
										_sm_ask_confirmation_1,
										transitions={'yes': 'yes', 'no': 'no', 'error': 'error', 'noname': 'noname'},
										autonomy={'yes': Autonomy.Inherit, 'no': Autonomy.Inherit, 'error': Autonomy.Inherit, 'noname': Autonomy.Inherit},
										remapping={'name': 'name'})

			# x:30 y:122
			OperatableStateMachine.add('look at',
										_sm_look_at_0,
										transitions={'finished': 'error'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'entity': 'entity'})



		with _state_machine:
			# x:62 y:38
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(Action_findPersonSM, 'Action_findPerson'),
										transitions={'done': 'If need the one', 'pas_done': 'reset Head'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'entity'})

			# x:818 y:362
			OperatableStateMachine.add('Do not find person',
										SaraSay(sentence="I did not find a person.", emotion=1, block=True),
										transitions={'done': 'cause2'},
										autonomy={'done': Autonomy.Off})

			# x:898 y:104
			OperatableStateMachine.add('Say found',
										SaraSayKey(Format=lambda x: "I have found " + x + "!", emotion=1, block=True),
										transitions={'done': 'get ID'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:200 y:536
			OperatableStateMachine.add('Retry',
										ForLoop(repeat=1),
										transitions={'do': 'Try again', 'end': 'reset Head'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:73 y:456
			OperatableStateMachine.add('Try again',
										SaraSay(sentence="Oh, I will try again.", emotion=1, block=True),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})

			# x:63 y:310
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'action_turn'),
										transitions={'finished': 'Action_findPerson', 'failed': 'reset Head'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:145 y:194
			OperatableStateMachine.add('reset Head',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'Do not find person'},
										autonomy={'done': Autonomy.Off})

			# x:1331 y:277
			OperatableStateMachine.add('set param',
										SetRosParam(ParamName="/behavior/FoundPerson/Id"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:1323 y:173
			OperatableStateMachine.add('get ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'set param'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'ID'})

			# x:689 y:44
			OperatableStateMachine.add('confirm and look at',
										_sm_confirm_and_look_at_3,
										transitions={'yes': 'Say found', 'no': 'Retry', 'error': 'reset Head', 'noname': 'get ID'},
										autonomy={'yes': Autonomy.Inherit, 'no': Autonomy.Inherit, 'error': Autonomy.Inherit, 'noname': Autonomy.Inherit},
										remapping={'name': 'name', 'entity': 'entity'})

			# x:904 y:464
			OperatableStateMachine.add('cause2',
										SetKey(Value="I did not find any person."),
										transitions={'done': 'setrosparamfailure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:1054 y:466
			OperatableStateMachine.add('setrosparamfailure',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:823 y:188
			OperatableStateMachine.add('say found person',
										SaraSay(sentence="I found a person.", emotion=1, block=True),
										transitions={'done': 'get ID'},
										autonomy={'done': Autonomy.Off})

			# x:529 y:21
			OperatableStateMachine.add('say hello',
										SaraSay(sentence="Hello.", emotion=1, block=True),
										transitions={'done': 'confirm and look at'},
										autonomy={'done': Autonomy.Off})

			# x:327 y:42
			OperatableStateMachine.add('If need the one',
										_sm_if_need_the_one_2,
										transitions={'done': 'say hello', 'no_param': 'say found person'},
										autonomy={'done': Autonomy.Inherit, 'no_param': Autonomy.Inherit},
										remapping={'Action': 'Action', 'person': 'person', 'name': 'name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
