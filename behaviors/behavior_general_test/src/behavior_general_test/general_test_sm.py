#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_general_test')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from sara_flexbe_states.GetRosParam import GetRosParam
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue May 01 2018
@author: Philippe La Madeleine
'''
class General_testSM(Behavior):
	'''
	made to test stuff
	'''


	def __init__(self):
		super(General_testSM, self).__init__()
		self.name = 'General_test'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:904 y:72, x:913 y:361
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Value = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:59 y:32
			OperatableStateMachine.add('start',
										LogState(text="Starting test", severity=Logger.REPORT_HINT),
										transitions={'done': 'f'},
										autonomy={'done': Autonomy.Off})

			# x:791 y:38
			OperatableStateMachine.add('success',
										LogState(text="test succeed", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:792 y:309
			OperatableStateMachine.add('fail',
										LogState(text="test failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:473 y:113
			OperatableStateMachine.add('f',
										GetRosParam(ParamName="test_param"),
										transitions={'done': 'success', 'failed': 'fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Value'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
