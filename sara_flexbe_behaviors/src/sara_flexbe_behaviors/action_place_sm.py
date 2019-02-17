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
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.log_state import LogState
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
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

		# O 36 311 
		# Gen Grip pose|n|nA

		# O 21 445 
		# MoveIt move|nmove = false|n|nPos

		# O 7 186 
		# PreGrip Pose #pre grip

		# O 18 372 
		# #approach_pos|nGen Grip pose|ndistance = 0.25

		# O 344 635 
		# MoveIt move|nmove =True|n|nA

		# O 613 634 
		# open grip

		# O 33 577 
		# MoveIt move|nmove =True|n|nB

		# O 766 629 
		# MoveIt move|n|nB

		# O 1087 628 
		# #preGrip|nMoveIt move



	def create(self):
		# x:1108 y:375, x:649 y:312
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


		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_get_down_3 = ConcurrencyContainer(outcomes=['done'], input_keys=['GripPose'], conditions=[
										('done', [('Go down', 'done')]),
										('done', [('read torque', 'done')])
										])

		with _sm_get_down_3:
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



		with _state_machine:
			# x:148 y:34
			OperatableStateMachine.add('TF_transformation',
										TF_transformation(in_ref="map", out_ref="base_link"),
										transitions={'done': 'LOG POSE', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'pos', 'out_pos': 'pos'})

			# x:144 y:299
			OperatableStateMachine.add('Gen place_pos',
										GenGripperPose(l=0, z=-0.05, planar=True),
										transitions={'done': 'Gen approach_pos', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'grip_pose'})

			# x:133 y:676
			OperatableStateMachine.add('Move_approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Get_down', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:150 y:231
			OperatableStateMachine.add('gotoPreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Gen place_pos', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:124 y:435
			OperatableStateMachine.add('MoveIt_isReachable',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'log app', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'grip_pose'})

			# x:148 y:165
			OperatableStateMachine.add('setPreGripPose',
										SetKey(Value="PrePlacePose"),
										transitions={'done': 'gotoPreGrip'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'PreGripPose'})

			# x:131 y:367
			OperatableStateMachine.add('Gen approach_pos',
										GenGripperPose(l=0.0, z=0.20, planar=True),
										transitions={'done': 'log place pos', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'approach_pose'})

			# x:739 y:581
			OperatableStateMachine.add('ReturnApproachPose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'genpose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:812 y:352
			OperatableStateMachine.add('ReturnPreGrip',
										MoveitMove(move=True, waitForExecution=False, group="RightArm"),
										transitions={'done': 'back', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:151 y:101
			OperatableStateMachine.add('LOG POSE',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'setPreGripPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'pos'})

			# x:137 y:506
			OperatableStateMachine.add('log app',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'look down'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'approach_pose'})

			# x:590 y:586
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.14, effort=1),
										transitions={'object': 'ReturnApproachPose', 'no_object': 'ReturnApproachPose'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:923 y:585
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'finished', 'no_object': 'finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:321 y:579
			OperatableStateMachine.add('Get_down',
										_sm_get_down_3,
										transitions={'done': 'say touchdown'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'GripPose': 'grip_pose'})

			# x:287 y:397
			OperatableStateMachine.add('log place pos',
										LogKeyState(text="place pose is {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'MoveIt_isReachable'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'grip_pose'})

			# x:463 y:518
			OperatableStateMachine.add('say touchdown',
										SaraSay(sentence="Touchdown!", input_keys=[], emotion=1, block=False),
										transitions={'done': 'open gripper'},
										autonomy={'done': Autonomy.Off})

			# x:923 y:480
			OperatableStateMachine.add('back',
										SaraRelMoveBase(),
										transitions={'arrived': 'close gripper', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'backPose'})

			# x:759 y:473
			OperatableStateMachine.add('genpose',
										GenPoseEuler(x=-0.3, y=-0.3, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'ReturnPreGrip'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'backPose'})

			# x:132 y:586
			OperatableStateMachine.add('look down',
										SaraSetHeadAngle(pitch=0.6, yaw=-0.3),
										transitions={'done': 'Move_approach'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
