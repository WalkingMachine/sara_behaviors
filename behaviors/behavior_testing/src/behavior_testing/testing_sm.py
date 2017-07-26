#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testing')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.int_topic_publisher import PublishInt
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 20 2017
@author: Redouane Laref
'''
class testingSM(Behavior):
	'''
	This is a test behavior
	'''


	def __init__(self):
		super(testingSM, self).__init__()
		self.name = 'testing'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:351 y:413
		_state_machine = OperatableStateMachine(outcomes=['done'], input_keys=['data', 'topic'])
		_state_machine.userdata.data = "2"
		_state_machine.userdata.topic = "essai"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:292 y:105
			OperatableStateMachine.add('publieur',
										PublishInt(),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'topic': 'topic', 'data': 'data'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
