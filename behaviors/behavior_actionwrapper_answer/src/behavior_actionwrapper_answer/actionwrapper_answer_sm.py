#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_answer')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 160 33 
		# ["Answer"]|nIl faut demander à se faire poser la question.



	def create(self):
		# x:30 y:324, x:130 y:324
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:89 y:97
			OperatableStateMachine.add('dummy wait',
										WaitState(wait_time=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]