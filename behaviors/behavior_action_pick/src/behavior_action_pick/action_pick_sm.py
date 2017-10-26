#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_expression import SetExpression
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.move_arm_pose import MoveArmPose
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
from behavior_check_reachability.check_reachability_sm import Check_reachabilitySM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.for_loop import ForLoop
from behavior_action_get_entity_pose.action_get_entity_pose_sm import Action_get_entity_poseSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Action_pickSM(Behavior):
	'''
	Try to pick an object
	'''


	def __init__(self):
		super(Action_pickSM, self).__init__()
		self.name = 'Action_pick'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Check_reachabilitySM, 'Check_reachability')
		self.add_behavior(Action_get_entity_poseSM, 'get_pose')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1079 y:346, x:572 y:212, x:613 y:428, x:581 y:89, x:717 y:247, x:1210 y:581
		_state_machine = OperatableStateMachine(outcomes=['success', 'too far', 'unreachable', 'not seen', 'critical fail', 'missed'], input_keys=['object'], output_keys=['grip_pose'])
		_state_machine.userdata.object = "cup"
		_state_machine.userdata.grip_pose = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:795 y:320, x:293 y:566
		_sm_get_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'], output_keys=['pose'])

		with _sm_get_0:
			# x:293 y:116
			OperatableStateMachine.add('gen1',
										GenGripperPose(x=0.04, y=0, z=0, t=0),
										transitions={'done': 'move1'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:297 y:441
			OperatableStateMachine.add('gen3',
										GenGripperPose(x=0.04, y=0, z=0, t=-0.5),
										transitions={'done': 'move3'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:519 y:135
			OperatableStateMachine.add('move1',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'gen2'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:524 y:306
			OperatableStateMachine.add('move2',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'gen3'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:528 y:462
			OperatableStateMachine.add('move3',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:296 y:282
			OperatableStateMachine.add('gen2',
										GenGripperPose(x=0.04, y=0, z=0, t=0.5),
										transitions={'done': 'move2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})


		# x:855 y:303, x:334 y:582
		_sm_approach_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'], output_keys=['pose'])

		with _sm_approach_1:
			# x:301 y:83
			OperatableStateMachine.add('gen1',
										GenGripperPose(x=-0.1, y=0, z=0, t=0),
										transitions={'done': 'say1'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:542 y:197
			OperatableStateMachine.add('move1',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'say2'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:334 y:294
			OperatableStateMachine.add('gen2',
										GenGripperPose(x=-0.1, y=-0.1, z=0, t=0.5),
										transitions={'done': 'move2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:543 y:364
			OperatableStateMachine.add('move2',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'say3'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:333 y:452
			OperatableStateMachine.add('gen3',
										GenGripperPose(x=-0.1, y=0.1, z=0, t=-0.5),
										transitions={'done': 'move3'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:543 y:494
			OperatableStateMachine.add('move3',
										MoveArmPose(wait=True),
										transitions={'done': 'finished', 'failed': 'say4'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:464 y:120
			OperatableStateMachine.add('say1',
										SaraSay(sentence="I will try to take it", emotion=1, block=False),
										transitions={'done': 'move1'},
										autonomy={'done': Autonomy.Off})

			# x:161 y:204
			OperatableStateMachine.add('say2',
										SaraSay(sentence="This is hard for me. Just wait a bit longer.", emotion=1, block=False),
										transitions={'done': 'gen2'},
										autonomy={'done': Autonomy.Off})

			# x:158 y:381
			OperatableStateMachine.add('say3',
										SaraSay(sentence="Almost there", emotion=1, block=False),
										transitions={'done': 'gen3'},
										autonomy={'done': Autonomy.Off})

			# x:448 y:554
			OperatableStateMachine.add('say4',
										SaraSay(sentence="Well, I didn't make it. Sorry.", emotion=1, block=False),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:438 y:64
			OperatableStateMachine.add('smile',
										SetExpression(emotion=1, brightness=999),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:50 y:414
			OperatableStateMachine.add('approach',
										_sm_approach_1,
										transitions={'finished': 'Get', 'failed': 'back'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:47 y:109
			OperatableStateMachine.add('PreGripPose',
										MoveArmNamedPose(pose_name="PreGripPose", wait=True),
										transitions={'done': 'get_pose', 'failed': 'sad'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:31 y:326
			OperatableStateMachine.add('Check_reachability',
										self.use_behavior(Check_reachabilitySM, 'Check_reachability'),
										transitions={'ok': 'approach', 'too_far': 'humm2'},
										autonomy={'ok': Autonomy.Inherit, 'too_far': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:52 y:503
			OperatableStateMachine.add('Get',
										_sm_get_0,
										transitions={'finished': 'gen up', 'failed': 'back2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:59 y:590
			OperatableStateMachine.add('gen up',
										GenGripperPose(x=0, y=0, z=0.05, t=0),
										transitions={'done': 'close'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:559 y:519
			OperatableStateMachine.add('move up',
										MoveArmPose(wait=True),
										transitions={'done': 'move back', 'failed': 'move back'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:729 y:519
			OperatableStateMachine.add('move back',
										MoveArmNamedPose(pose_name="PostGripPose", wait=True),
										transitions={'done': 'success', 'failed': 'critical fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:233 y:520
			OperatableStateMachine.add('close',
										SetGripperState(width=0, effort=0.00001),
										transitions={'object': 'got it', 'no_object': 'say fail 2'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:232 y:380
			OperatableStateMachine.add('back',
										MoveArmNamedPose(pose_name="PreGripPose", wait=False),
										transitions={'done': 'open gripper', 'failed': 'open gripper'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:229 y:447
			OperatableStateMachine.add('back2',
										MoveArmNamedPose(pose_name="PreGripPose", wait=False),
										transitions={'done': 'open gripper', 'failed': 'sad'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:52 y:255
			OperatableStateMachine.add('see it',
										SaraSay(sentence="I see it", emotion=1, block=True),
										transitions={'done': 'Check_reachability'},
										autonomy={'done': Autonomy.Off})

			# x:407 y:266
			OperatableStateMachine.add('too far s',
										SaraSay(sentence="But it is too far", emotion=1, block=True),
										transitions={'done': 'too far'},
										autonomy={'done': Autonomy.Off})

			# x:282 y:117
			OperatableStateMachine.add('say not seen',
										SaraSayKey(Format=lambda x: "I can't see the "+x, emotion=1, block=True),
										transitions={'done': 'smile'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'object'})

			# x:245 y:591
			OperatableStateMachine.add('say fail 2',
										SaraSay(sentence="Oops, I missed it.", emotion=1, block=False),
										transitions={'done': 'open 2'},
										autonomy={'done': Autonomy.Off})

			# x:913 y:573
			OperatableStateMachine.add('for',
										ForLoop(repeat=1),
										transitions={'do': 'again', 'end': 'move back 2'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:939 y:28
			OperatableStateMachine.add('again',
										SaraSay(sentence="Let me try again.", emotion=1, block=False),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:411 y:519
			OperatableStateMachine.add('got it',
										SaraSay(sentence="I got it", emotion=1, block=False),
										transitions={'done': 'move up'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:175
			OperatableStateMachine.add('get_pose',
										self.use_behavior(Action_get_entity_poseSM, 'get_pose'),
										transitions={'found': 'see it', 'not found': 'humm'},
										autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
										remapping={'name': 'object', 'pose': 'pose'})

			# x:386 y:570
			OperatableStateMachine.add('open 2',
										SetGripperState(width=0.15, effort=0),
										transitions={'object': 'for', 'no_object': 'for'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:1032 y:568
			OperatableStateMachine.add('move back 2',
										MoveArmNamedPose(pose_name="PreGripPose", wait=True),
										transitions={'done': 'missed', 'failed': 'missed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:789 y:354
			OperatableStateMachine.add('sad',
										SetExpression(emotion=2, brightness=999),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:26
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.14, effort=0),
										transitions={'object': 'PreGripPose', 'no_object': 'PreGripPose'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:668 y:138
			OperatableStateMachine.add('humm',
										SetExpression(emotion=3, brightness=999),
										transitions={'done': 'say not seen'},
										autonomy={'done': Autonomy.Off})

			# x:242 y:287
			OperatableStateMachine.add('humm2',
										SetExpression(emotion=3, brightness=999),
										transitions={'done': 'too far s'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
