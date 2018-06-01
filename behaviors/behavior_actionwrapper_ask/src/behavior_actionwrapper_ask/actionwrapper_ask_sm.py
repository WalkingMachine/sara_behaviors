#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_ask')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 27 2018
@author: Philippe La Madeleine
'''
class ActionWrapper_AskSM(Behavior):
	'''
	Ask something
	'''


	def __init__(self):
		super(ActionWrapper_AskSM, self).__init__()
		self.name = 'ActionWrapper_Ask'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 160 33 
		# ["Ask", "Question"]



	def create(self):
		# x:793 y:463, x:150 y:458, x:458 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = "Default question"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('fisrtSentence',
										SaraSay(sentence="Hello, I have a question for you.", emotion=1, block=True),
										transitions={'done': 'trouveLaQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:387 y:166
			OperatableStateMachine.add('AskTheQuestion',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'question'})

			# x:194 y:99
			OperatableStateMachine.add('trouveLaQuestion',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'question'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
