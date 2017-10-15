#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.get_marker import GetMarker
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.move_arm_pose import MoveArmPose
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe la Madeleine
'''
class Test_continueSM(Behavior):
	'''
	test the continue button
	'''


	def __init__(self):
		super(Test_continueSM, self).__init__()
		self.name = 'Test_continue'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:785 y:394, x:523 y:338
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:443 y:124
			OperatableStateMachine.add('gri',
										SetGripperState(width=0.05, effort=255),
										transitions={'object': 'close', 'no_object': 'close'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:142 y:92
			OperatableStateMachine.add('mm',
										GetMarker(index=15),
										transitions={'done': 'sss', 'not_found': 'say'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'pose': 'pose_in'})

			# x:49 y:200
			OperatableStateMachine.add('gg',
										GenGripperPose(x=-0.1, y=0, z=0),
										transitions={'done': 'p'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose_in', 'pose_out': 'pose_out'})

			# x:242 y:116
			OperatableStateMachine.add('sss',
										SaraSay(sentence="I see it. Let me take it", emotion=1, block=False),
										transitions={'done': 'gg'},
										autonomy={'done': Autonomy.Off})

			# x:69 y:286
			OperatableStateMachine.add('p',
										MoveArmPose(wait=True),
										transitions={'done': 'ggggg', 'failed': 'www'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:35 y:101
			OperatableStateMachine.add('say',
										SaraSay(sentence="show me a tag 15", emotion=1, block=True),
										transitions={'done': 'mm'},
										autonomy={'done': Autonomy.Off})

			# x:830 y:232
			OperatableStateMachine.add('ggg',
										SaraSay(sentence="got it", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:82 y:483
			OperatableStateMachine.add('ddddd',
										MoveArmPose(wait=True),
										transitions={'done': 'ssssss', 'failed': 'www'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:70 y:390
			OperatableStateMachine.add('ggggg',
										GenGripperPose(x=0, y=0, z=0),
										transitions={'done': 'ddddd'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose_in', 'pose_out': 'pose_out'})

			# x:390 y:300
			OperatableStateMachine.add('www',
										SaraSay(sentence="I can't reach it", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:658 y:146
			OperatableStateMachine.add('close',
										SetGripperState(width=0.0, effort=255),
										transitions={'object': 'ggg', 'no_object': 'says'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:489 y:517
			OperatableStateMachine.add('ssssss',
										MoveArmNamedPose(pose_name="IdlePose", wait=True),
										transitions={'done': 'say', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:660 y:245
			OperatableStateMachine.add('says',
										SaraSay(sentence="There is nothing in my hand", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
