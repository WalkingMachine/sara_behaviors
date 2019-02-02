#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.test_de_behavior_sm import testdebehaviorSM as sara_flexbe_behaviors__testdebehaviorSM
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class ATestSandboxSM(Behavior):
	'''
	Une behavior pour faire des tests rapidement.
	'''


	def __init__(self):
		super(ATestSandboxSM, self).__init__()
		self.name = 'A Test Sandbox'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__testdebehaviorSM, 'test de behavior')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:537 y:110, x:515 y:330
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PostGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.actionList = [["Find", "bottle"], ["move", "kitchen"]]
		_state_machine.userdata.titre = "test"
		_state_machine.userdata.relative = False
		_state_machine.userdata.pitch = -0.8
		_state_machine.userdata.Action1 = ["move", "counter"]
		_state_machine.userdata.Action2 = ["move", "table"]
		_state_machine.userdata.pose = "Dining room"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:134 y:83
			OperatableStateMachine.add('test de behavior',
										self.use_behavior(sara_flexbe_behaviors__testdebehaviorSM, 'test de behavior'),
										transitions={'finished': 'log', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:411 y:111
			OperatableStateMachine.add('log',
										LogState(text="ok", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
