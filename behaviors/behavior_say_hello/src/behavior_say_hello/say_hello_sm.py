#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_say_hello')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jul 19 2017
@author: Lucas Maurice
'''
class Say_HelloSM(Behavior):
	'''
	Just say Hello
	'''


	def __init__(self):
		super(Say_HelloSM, self).__init__()
		self.name = 'Say_Hello'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:94 y:85
			OperatableStateMachine.add('SaraSay',
										SaraSay(sentence="Hello, I'm Sara !", emotion=3),
										transitions={'done': 'WaitState'},
										autonomy={'done': Autonomy.Off})

			# x:277 y:84
			OperatableStateMachine.add('WaitState',
										WaitState(wait_time=2),
										transitions={'done': 'SaraSay'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
