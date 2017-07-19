#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_stop')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.FIFO_New import FIFO_New
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 15 2017
@author: Lucas Maurice
'''
class StopSM(Behavior):
	'''
	Empty all FIFOs.
	'''


	def __init__(self):
		super(StopSM, self).__init__()
		self.name = 'Stop'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:171 y:361
		_state_machine = OperatableStateMachine(outcomes=['finished'], output_keys=['high_fifo', 'med_fifo', 'low_fifo'])
		_state_machine.userdata.high_fifo = []
		_state_machine.userdata.med_fifo = []
		_state_machine.userdata.low_fifo = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('New High FIFO',
										FIFO_New(),
										transitions={'done': 'New Med FIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'high_fifo'})

			# x:73 y:144
			OperatableStateMachine.add('New Med FIFO',
										FIFO_New(),
										transitions={'done': 'New Low FIFO'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'med_fifo'})

			# x:102 y:250
			OperatableStateMachine.add('New Low FIFO',
										FIFO_New(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'low_fifo'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
