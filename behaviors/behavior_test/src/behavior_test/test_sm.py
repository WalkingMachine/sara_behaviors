#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.move_joint import MoveJoint
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 20 2017
@author: Redouane Laref
'''
class TESTSM(Behavior):
	'''
	This is a test behavior
	'''


	def __init__(self):
		super(TESTSM, self).__init__()
		self.name = 'TEST'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:351 y:413
		_state_machine = OperatableStateMachine(outcomes=['finished'], input_keys=['data', 'topic'])
		_state_machine.userdata.data = "2.5"
		_state_machine.userdata.topic = "test"
		_state_machine.userdata.pose_name = "idlepose"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:188 y:176
			OperatableStateMachine.add('test_movejoint',
										MoveJoint(pose_name="IdlePose"),
										transitions={'done': 'finished', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
