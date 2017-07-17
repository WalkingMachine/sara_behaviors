#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_test')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
from flexbe_states.log_state import LogState
from sara_flexbe_states.sara_say_key import SaraSayKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 16 2017
@author: Wonderland_Test
'''
class Wonderland_TestSM(Behavior):
	'''
	Wonderland_Test
	'''


	def __init__(self):
		super(Wonderland_TestSM, self).__init__()
		self.name = 'Wonderland_Test'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.url = "entity"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:315 y:123
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'say', 'error': 'Log'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'response'})

			# x:568 y:255
			OperatableStateMachine.add('Log',
										LogState(text="Wonderland Request Failed.", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:25 y:192
			OperatableStateMachine.add('say',
										SaraSayKey(Format=lambda x: x, emotion=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'response'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
