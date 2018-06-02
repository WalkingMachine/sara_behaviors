#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_answer')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.for_loop import ForLoop
from flexbe_states.calculation_state import CalculationState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 336 25 
		# ["Answer"]|nIl faut demander à se faire poser la question.



	def create(self):
		# x:748 y:626, x:66 y:470, x:371 y:623
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


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
										transitions={'done': 'AskIfQuestion', 'pas_done': 'noPerson'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'personClass', 'entity': 'entity'})

			# x:45 y:227
			OperatableStateMachine.add('noPerson',
										SaraSay(sentence="I can't find any person here.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:409 y:108
			OperatableStateMachine.add('getResponse',
										GetSpeech(watchdog=7),
										transitions={'done': 'calculResponse', 'nothing': 'looping', 'fail': 'looping'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'response'})

			# x:386 y:242
			OperatableStateMachine.add('looping',
										ForLoop(repeat=1),
										transitions={'do': 'sayRepeat', 'end': 'NotUnderstandEnd'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:256 y:224
			OperatableStateMachine.add('sayRepeat',
										SaraSay(sentence="I did'nt understand. Do you have a question for me?", emotion=1, block=True),
										transitions={'done': 'getResponse'},
										autonomy={'done': Autonomy.Off})

			# x:195 y:357
			OperatableStateMachine.add('NotUnderstandEnd',
										SaraSay(sentence="Sorry. I can't understand your response.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:574 y:117
			OperatableStateMachine.add('calculResponse',
										CalculationState(calculation=lambda x: "yes" in x),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'response', 'output_value': 'output_value'})

			# x:243 y:116
			OperatableStateMachine.add('AskIfQuestion',
										SaraSay(sentence="Hello. Do you have a question for me?", emotion=1, block=True),
										transitions={'done': 'getResponse'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
