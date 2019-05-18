#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 04 2019
@author: Quentin Gaillot
'''
class Action_AskSM(Behavior):
	'''
	Ask a question to a person already in front of the robot and return the answer
	'''


	def __init__(self):
		super(Action_AskSM, self).__init__()
		self.name = 'Action_Ask'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1013 y:314, x:1017 y:162
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['question'], output_keys=['answer'])
		_state_machine.userdata.question = ""
		_state_machine.userdata.answer = ""

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:79 y:95
			OperatableStateMachine.add('say question',
										SaraSay(sentence=lambda x: "x[0]", input_keys=["question"], emotion=0, block=True),
										transitions={'done': 'get answer'},
										autonomy={'done': Autonomy.Off},
										remapping={'question': 'question'})

			# x:92 y:304
			OperatableStateMachine.add('get answer',
										GetSpeech(watchdog=10),
										transitions={'done': 'finished', 'nothing': 'retry ask', 'fail': 'retry ask'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'answer'})

			# x:345 y:202
			OperatableStateMachine.add('retry ask',
										ForLoop(repeat=2),
										transitions={'do': 'say not understand', 'end': 'say failed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:232 y:90
			OperatableStateMachine.add('say not understand',
										SaraSay(sentence="Sorry, I did not understand your answer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'say question'},
										autonomy={'done': Autonomy.Off})

			# x:604 y:151
			OperatableStateMachine.add('say failed',
										SaraSay(sentence="Sorry, I can't understand your answer.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
