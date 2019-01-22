#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_a_test_sandbox')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from flexbe_states.log_state import LogState
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_actionwrapper_follow.actionwrapper_follow_sm import ActionWrapper_FollowSM
from behavior_actionwrapper_find_person.actionwrapper_find_person_sm import ActionWrapper_Find_PersonSM
from sara_flexbe_states.get_speech import GetSpeech
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
		self.add_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move')
		self.add_behavior(ActionWrapper_FollowSM, 'ActionWrapper_Follow')
		self.add_behavior(ActionWrapper_Find_PersonSM, 'ActionWrapper_Find_Person')
		self.add_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:929 y:535, x:515 y:330
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
			# x:182 y:536
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move'),
										transitions={'finished': 'ActionWrapper_Move_2', 'failed': 'ActionWrapper_Move_2', 'critical_fail': 'ActionWrapper_Move_2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action1'})

			# x:416 y:237
			OperatableStateMachine.add('Failure',
										LogState(text="The test is a failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:724 y:32
			OperatableStateMachine.add('success',
										LogState(text="The test is a success", severity=Logger.REPORT_HINT),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:510 y:69
			OperatableStateMachine.add('Move2',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'move', 'failed': 'Failure'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose2'})

			# x:313 y:56
			OperatableStateMachine.add('move',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Move2', 'failed': 'Failure'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose1'})

			# x:362 y:325
			OperatableStateMachine.add('sa',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'gg'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'words'})

			# x:593 y:441
			OperatableStateMachine.add('ActionWrapper_Follow',
										self.use_behavior(ActionWrapper_FollowSM, 'ActionWrapper_Follow'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action2'})

			# x:205 y:416
			OperatableStateMachine.add('ActionWrapper_Find_Person',
										self.use_behavior(ActionWrapper_Find_PersonSM, 'ActionWrapper_Find_Person'),
										transitions={'finished': 'ActionWrapper_Follow', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action1'})

			# x:629 y:555
			OperatableStateMachine.add('ActionWrapper_Move_2',
										self.use_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move_2'),
										transitions={'finished': 'ActionWrapper_Move', 'failed': 'ActionWrapper_Move', 'critical_fail': 'ActionWrapper_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action2'})

			# x:216 y:319
			OperatableStateMachine.add('gg',
										GetSpeech(watchdog=10),
										transitions={'done': 'sa', 'nothing': 'gg', 'fail': 'gg'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
