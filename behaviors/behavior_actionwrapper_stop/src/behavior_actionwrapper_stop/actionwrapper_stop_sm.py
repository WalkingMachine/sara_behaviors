#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_stop')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_stop.stop_sm import StopSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jul 15 2017
@author: Lucas Maurice
'''
class ActionWrapper_StopSM(Behavior):
	'''
	Enveloppe de l'action Stop
	'''


	def __init__(self):
		super(ActionWrapper_StopSM, self).__init__()
		self.name = 'ActionWrapper_Stop'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(StopSM, 'Stop')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
		_state_machine.userdata.Action = ['Stop']

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:55 y:116
			OperatableStateMachine.add('Stop',
										self.use_behavior(StopSM, 'Stop'),
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'high_fifo': 'high_fifo', 'med_fifo': 'med_fifo', 'low_fifo': 'low_fifo'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
