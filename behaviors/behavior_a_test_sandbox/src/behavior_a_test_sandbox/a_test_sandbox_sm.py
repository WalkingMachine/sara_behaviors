#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_sandbox')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
from behavior_actionwrapper_place.actionwrapper_place_sm import ActionWrapper_PlaceSM
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
		self.add_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick')
		self.add_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:824 y:62, x:824 y:212
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PreGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.Action = ["", "bottle"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:120 y:64
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick'),
										transitions={'finished': 'ActionWrapper_Place', 'failed': 'Failure', 'critical_fail': 'Failure'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:718 y:180
			OperatableStateMachine.add('Failure',
										LogState(text="The test is a failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:388 y:20
			OperatableStateMachine.add('ActionWrapper_Place',
										self.use_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place'),
										transitions={'finished': 'success', 'failed': 'Failure', 'critical_fail': 'Failure'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:725 y:32
			OperatableStateMachine.add('success',
										LogState(text="The test is a success", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
