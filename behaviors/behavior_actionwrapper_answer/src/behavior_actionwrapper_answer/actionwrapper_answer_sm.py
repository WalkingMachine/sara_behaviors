#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_answer')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_nlu_spr import SaraNLUspr
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.for_loop import ForLoop
from flexbe_states.check_condition_state import CheckConditionState
from behavior_action_turn.action_turn_sm import action_turnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 27 2018
@author: Philippe La Madeleine
'''
class ActionWrapper_AnswerSM(Behavior):
	'''
	Answer a question
	'''


	def __init__(self):
		super(ActionWrapper_AnswerSM, self).__init__()
		self.name = 'ActionWrapper_Answer'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_findPersonSM, 'Action_findPerson')
		self.add_behavior(action_turnSM, 'turnToFindAnotherPersonOnce/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 161 5 
		# ["Answer"]|nIl faut demander à se faire poser la question.



	def create(self):
		# x:317 y:570, x:691 y:132, x:589 y:443
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365
		_sm_turntofindanotherpersononce_0 = OperatableStateMachine(outcomes=['end', 'finished', 'failed'])

		with _sm_turntofindanotherpersononce_0:
			# x:32 y:135
			OperatableStateMachine.add('sayNeverMind',
										SaraSay(sentence="OK. Never mind", emotion=1, block=True),
										transitions={'done': 'loopFindOtherPerson'},
										autonomy={'done': Autonomy.Off})

			# x:156 y:151
			OperatableStateMachine.add('loopFindOtherPerson',
										ForLoop(repeat=1),
										transitions={'do': 'SetRotation', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index3'})

			# x:30 y:40
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'turnToFindAnotherPersonOnce/action_turn'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation'})

			# x:194 y:86
			OperatableStateMachine.add('SetRotation',
										SetKey(Value=3.1416),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'rotation'})


		# x:196 y:458, x:495 y:340
		_sm_listenandstorethequestion_1 = OperatableStateMachine(outcomes=['done', 'end'], output_keys=['operatorQuestion'])

		with _sm_listenandstorethequestion_1:
			# x:30 y:51
			OperatableStateMachine.add('sayAskQuestion',
										SaraSay(sentence="Ask me your question please.", emotion=1, block=True),
										transitions={'done': 'getQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:194
			OperatableStateMachine.add('getQuestion',
										GetSpeech(watchdog=7),
										transitions={'done': 'done', 'nothing': 'looping2', 'fail': 'looping2'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'operatorQuestion'})

			# x:250 y:262
			OperatableStateMachine.add('looping2',
										ForLoop(repeat=1),
										transitions={'do': 'sayRepeat2', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index2'})

			# x:273 y:94
			OperatableStateMachine.add('sayRepeat2',
										SaraSay(sentence="I did'nt understand. Can you repeat please?", emotion=1, block=True),
										transitions={'done': 'getQuestion'},
										autonomy={'done': Autonomy.Off})


		# x:137 y:546, x:475 y:361, x:494 y:244
		_sm_ifquestionforsara_2 = OperatableStateMachine(outcomes=['true', 'false', 'end'])

		with _sm_ifquestionforsara_2:
			# x:30 y:40
			OperatableStateMachine.add('AskIfQuestion',
										SaraSay(sentence="Hello. Do you have a question for me?", emotion=1, block=True),
										transitions={'done': 'getResponse'},
										autonomy={'done': Autonomy.Off})

			# x:23 y:108
			OperatableStateMachine.add('getResponse',
										GetSpeech(watchdog=7),
										transitions={'done': 'ifYes', 'nothing': 'looping', 'fail': 'looping'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'response'})

			# x:261 y:216
			OperatableStateMachine.add('looping',
										ForLoop(repeat=1),
										transitions={'do': 'sayRepeat', 'end': 'end'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:254 y:63
			OperatableStateMachine.add('sayRepeat',
										SaraSay(sentence="I did'nt understand. Do you have a question for me?", emotion=1, block=True),
										transitions={'done': 'getResponse'},
										autonomy={'done': Autonomy.Off})

			# x:73 y:394
			OperatableStateMachine.add('ifYes',
										CheckConditionState(predicate=lambda x: "yes" in x or "sure" in x or "of course" in x),
										transitions={'true': 'true', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'response'})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('SetPersonClass',
										SetKey(Value="person"),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personClass'})

			# x:20 y:117
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(Action_findPersonSM, 'Action_findPerson'),
										transitions={'done': 'IfQuestionForSARA', 'pas_done': 'noPerson'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'personClass', 'entity': 'entity'})

			# x:374 y:60
			OperatableStateMachine.add('noPerson',
										SaraSay(sentence="I can't find any person here.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:338 y:399
			OperatableStateMachine.add('NotUnderstandEnd',
										SaraSay(sentence="Sorry. I can't understand your answer.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:39 y:384
			OperatableStateMachine.add('SendToNLU',
										SaraNLUspr(),
										transitions={'understood': 'findResponseString', 'not_understood': 'CannotAnswer', 'fail': 'CannotAnswer'},
										autonomy={'understood': Autonomy.Off, 'not_understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'operatorQuestion', 'ActionForms': 'ActionForms'})

			# x:353 y:454
			OperatableStateMachine.add('CannotAnswer',
										SaraSay(sentence="Sorry. I can't answer your question.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:27 y:465
			OperatableStateMachine.add('findResponseString',
										CalculationState(calculation=lambda x: x.data),
										transitions={'done': 'sayAnswer'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'ActionForms', 'output_value': 'stringAnswer'})

			# x:38 y:546
			OperatableStateMachine.add('sayAnswer',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'stringAnswer'})

			# x:23 y:208
			OperatableStateMachine.add('IfQuestionForSARA',
										_sm_ifquestionforsara_2,
										transitions={'true': 'ListenAndStoreTheQuestion', 'false': 'turnToFindAnotherPersonOnce', 'end': 'NotUnderstandEnd'},
										autonomy={'true': Autonomy.Inherit, 'false': Autonomy.Inherit, 'end': Autonomy.Inherit})

			# x:16 y:298
			OperatableStateMachine.add('ListenAndStoreTheQuestion',
										_sm_listenandstorethequestion_1,
										transitions={'done': 'SendToNLU', 'end': 'NotUnderstandEnd'},
										autonomy={'done': Autonomy.Inherit, 'end': Autonomy.Inherit},
										remapping={'operatorQuestion': 'operatorQuestion'})

			# x:299 y:169
			OperatableStateMachine.add('turnToFindAnotherPersonOnce',
										_sm_turntofindanotherpersononce_0,
										transitions={'end': 'failed', 'finished': 'Action_findPerson', 'failed': 'failed'},
										autonomy={'end': Autonomy.Inherit, 'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
