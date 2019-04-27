#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.TF_transform import TF_transformation
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.moveit_move import MoveitMove
from flexbe_states.log_state import LogState
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Raphael Duchaine
'''
class Action_placeSM(Behavior):
	'''
	Place un objet a une position
	'''


	def __init__(self):
		super(Action_placeSM, self).__init__()
		self.name = 'Action_place'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 52 47 
		# TF Transform |nFrame1 Frame2|n

		# O 36 230 
		# Gen Grip pose|n|nA

		# O 33 308 
		# MoveIt move|nmove = false|n|nPos

		# O 6 135 
		# PreGrip Pose #pre grip

		# O 27 264 
		# #approach_pos|nGen Grip pose|ndistance = 0.25

		# O 0 491 
		# MoveIt move|nmove =True|n|nA

		# O 300 580 
		# open grip

		# O 36 446 
		# MoveIt move|nmove =True|n|nB

		# O 473 575 
		# MoveIt move|n|nB

		# O 460 491 
		# #preGrip|nMoveIt move



	def create(self):
		# x:682 y:306, x:452 y:252
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pos'])
		_state_machine.userdata.pos = {"x":0.8, "y":-0.2, "z":1}

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458, x:230 y:458, x:330 y:458, x:430 y:458, x:530 y:458, x:630 y:458, x:59 y:533, x:830 y:458
		_sm_group_0 = ConcurrencyContainer(outcomes=['threshold', 'watchdog', 'fail'], conditions=[
										('threshold', [('read', 'threshold')]),
										('watchdog', [('read', 'watchdog')]),
										('fail', [('read', 'fail')]),
										('threshold', [('read yaw', 'threshold')]),
										('fail', [('read yaw', 'fail')]),
										('watchdog', [('read yaw', 'watchdog')])
										])

		with _sm_group_0:
			# x:86 y:125
			OperatableStateMachine.add('read',
										ReadTorque(watchdog=1, Joint="right_elbow_pitch_joint", Threshold=0.7, min_time=0.4),
										transitions={'threshold': 'threshold', 'watchdog': 'watchdog', 'fail': 'fail'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:252 y:135
			OperatableStateMachine.add('read yaw',
										ReadTorque(watchdog=1, Joint="right_elbow_pitch_joint", Threshold=0.5, min_time=0.4),
										transitions={'threshold': 'threshold', 'watchdog': 'watchdog', 'fail': 'fail'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})


		# x:30 y:458
		_sm_read_torque_1 = OperatableStateMachine(outcomes=['done'])

		with _sm_read_torque_1:
			# x:142 y:61
			OperatableStateMachine.add('log',
										LogState(text="going down", severity=Logger.REPORT_HINT),
										transitions={'done': 'Group'},
										autonomy={'done': Autonomy.Off})

			# x:131 y:164
			OperatableStateMachine.add('Group',
										_sm_group_0,
										transitions={'threshold': 'done', 'watchdog': 'log', 'fail': 'done'},
										autonomy={'threshold': Autonomy.Inherit, 'watchdog': Autonomy.Inherit, 'fail': Autonomy.Inherit})


		# x:30 y:458
		_sm_go_down_2 = OperatableStateMachine(outcomes=['done'], input_keys=['GripPose'])

		with _sm_go_down_2:
			# x:126 y:194
			OperatableStateMachine.add('movePlace',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'done'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'GripPose'})


		# x:30 y:324, x:130 y:324
		_sm_retreate_arm_3 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['approach_pose', 'PreGripPose'])

		with _sm_retreate_arm_3:
			# x:30 y:40
			OperatableStateMachine.add('ReturnApproachPose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'ReturnPreGrip', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:202 y:41
			OperatableStateMachine.add('ReturnPreGrip',
										MoveitMove(move=True, waitForExecution=False, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})


		# x:30 y:324, x:130 y:324
		_sm_releasing_4 = OperatableStateMachine(outcomes=['object', 'no_object'])

		with _sm_releasing_4:
			# x:30 y:40
			OperatableStateMachine.add('say touchdown',
										SaraSay(sentence="Touchdown!", input_keys=[], emotion=1, block=False),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:139 y:176
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.14, effort=1),
										transitions={'object': 'object', 'no_object': 'no_object'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		# x:30 y:324, x:130 y:324
		_sm_moveback_5 = OperatableStateMachine(outcomes=['arrived', 'failed'])

		with _sm_moveback_5:
			# x:30 y:40
			OperatableStateMachine.add('genpose',
										GenPoseEuler(x=-0.3, y=-0.3, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'move back'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'backPose'})

			# x:40 y:163
			OperatableStateMachine.add('move back',
										SaraMoveBase(reference="base_link"),
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'backPose'})


		# x:536 y:72, x:231 y:292
		_sm_prepare_grip_6 = OperatableStateMachine(outcomes=['failed', 'done'], input_keys=['pos'], output_keys=['approach_pose', 'grip_pose'])

		with _sm_prepare_grip_6:
			# x:50 y:40
			OperatableStateMachine.add('Gen place_pos',
										GenGripperPose(l=0, z=-0.05, planar=True),
										transitions={'done': 'Gen approach_pos', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'grip_pose'})

			# x:30 y:176
			OperatableStateMachine.add('MoveIt_isReachable',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'log app', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grip_pose'})

			# x:37 y:108
			OperatableStateMachine.add('Gen approach_pos',
										GenGripperPose(l=0.0, z=0.20, planar=True),
										transitions={'done': 'log place pos', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'approach_pose'})

			# x:41 y:269
			OperatableStateMachine.add('log app',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'approach_pose'})

			# x:360 y:180
			OperatableStateMachine.add('log place pos',
										LogKeyState(text="place pose is {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'MoveIt_isReachable'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'grip_pose'})


		# x:30 y:324, x:130 y:324
		_sm_pregrippose_7 = OperatableStateMachine(outcomes=['done', 'failed'], output_keys=['PreGripPose'])

		with _sm_pregrippose_7:
			# x:30 y:40
			OperatableStateMachine.add('setPreGripPose',
										SetKey(Value="PrePlacePose"),
										transitions={'done': 'gotoPreGrip'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'PreGripPose'})

			# x:32 y:106
			OperatableStateMachine.add('gotoPreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})


		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_get_down_8 = ConcurrencyContainer(outcomes=['done'], input_keys=['GripPose'], conditions=[
										('done', [('Go down', 'done')]),
										('done', [('read torque', 'done')])
										])

		with _sm_get_down_8:
			# x:178 y:127
			OperatableStateMachine.add('Go down',
										_sm_go_down_2,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'GripPose': 'GripPose'})

			# x:405 y:150
			OperatableStateMachine.add('read torque',
										_sm_read_torque_1,
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Inherit})


		# x:30 y:324, x:130 y:324
		_sm_pretraitement_9 = OperatableStateMachine(outcomes=['fail', 'done'], input_keys=['pos'], output_keys=['pos'])

		with _sm_pretraitement_9:
			# x:30 y:40
			OperatableStateMachine.add('TF_transformation',
										TF_transformation(in_ref="map", out_ref="base_link"),
										transitions={'done': 'LOG POSE', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'pos', 'out_pos': 'pos'})

			# x:33 y:107
			OperatableStateMachine.add('LOG POSE',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'pos'})



		with _state_machine:
			# x:148 y:34
			OperatableStateMachine.add('Pretraitement',
										_sm_pretraitement_9,
										transitions={'fail': 'failed', 'done': 'PreGripPose'},
										autonomy={'fail': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'pos': 'pos'})

			# x:634 y:410
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'finished', 'no_object': 'finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:141 y:522
			OperatableStateMachine.add('Get_down',
										_sm_get_down_8,
										transitions={'done': 'releasing'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'GripPose': 'grip_pose'})

			# x:159 y:352
			OperatableStateMachine.add('look down',
										SaraSetHeadAngle(pitch=0.6, yaw=-0.3),
										transitions={'done': 'Move_approach'},
										autonomy={'done': Autonomy.Off})

			# x:160 y:127
			OperatableStateMachine.add('PreGripPose',
										_sm_pregrippose_7,
										transitions={'done': 'Prepare grip', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'PreGripPose': 'PreGripPose'})

			# x:156 y:238
			OperatableStateMachine.add('Prepare grip',
										_sm_prepare_grip_6,
										transitions={'failed': 'failed', 'done': 'look down'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'pos': 'pos', 'approach_pose': 'approach_pose', 'grip_pose': 'grip_pose'})

			# x:139 y:444
			OperatableStateMachine.add('Move_approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Get_down', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:623 y:525
			OperatableStateMachine.add('Moveback',
										_sm_moveback_5,
										transitions={'arrived': 'close gripper', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:298 y:520
			OperatableStateMachine.add('releasing',
										_sm_releasing_4,
										transitions={'object': 'retreate arm', 'no_object': 'retreate arm'},
										autonomy={'object': Autonomy.Inherit, 'no_object': Autonomy.Inherit})

			# x:459 y:522
			OperatableStateMachine.add('retreate arm',
										_sm_retreate_arm_3,
										transitions={'failed': 'failed', 'done': 'Moveback'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'approach_pose': 'approach_pose', 'PreGripPose': 'PreGripPose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
