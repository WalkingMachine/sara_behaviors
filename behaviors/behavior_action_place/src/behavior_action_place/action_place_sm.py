#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.log_key_state import LogKeyState
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

		# O 34 61 
		# TF Transform |nFrame1 Frame2|n

		# O 316 715 
		# Gen Grip pose|n|nA

		# O 25 171 
		# MoveIt move|nmove = false|n|nPos

		# O 0 336 
		# PreGrip Pose #pre grip

		# O 0 393 
		# #approach_pos|nGen Grip pose|ndistance = 0.25

		# O 560 732 
		# MoveIt move|nmove =True|n|nA

		# O 709 702 
		# open grip

		# O 0 634 
		# MoveIt move|nmove =True|n|nB

		# O 832 701 
		# MoveIt move|n|nB

		# O 1076 687 
		# #preGrip|nMoveIt move



	def create(self):
		# x:1241 y:596, x:728 y:387
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pos'])
		_state_machine.userdata.pos = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:148 y:34
			OperatableStateMachine.add('TF_transformation',
										TF_transformation(in_ref="map", out_ref="base_link"),
										transitions={'done': 'LOG POSE', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'in_pos': 'pos', 'out_pos': 'pos'})

			# x:328 y:641
			OperatableStateMachine.add('Gen place_pos',
										GenGripperPose(l=0.0, z=0, planar=True),
										transitions={'done': 'setOpened', 'fail': 'Gen place_pos'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'grip_pose'})

			# x:103 y:633
			OperatableStateMachine.add('Move_approach',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Gen place_pos', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:168 y:322
			OperatableStateMachine.add('gotoPreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Gen approach_pos', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:124 y:178
			OperatableStateMachine.add('MoveIt_isReachable',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'setPreGripPose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pos'})

			# x:120 y:251
			OperatableStateMachine.add('setPreGripPose',
										SetKey(Value="PreGripPose"),
										transitions={'done': 'gotoPreGrip'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'PreGripPose'})

			# x:714 y:650
			OperatableStateMachine.add('Open_grip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'ReturnApproachPose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Opened'})

			# x:549 y:651
			OperatableStateMachine.add('setOpened',
										SetKey(Value="Opened"),
										transitions={'done': 'Open_grip'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Opened'})

			# x:133 y:391
			OperatableStateMachine.add('Gen approach_pos',
										GenGripperPose(l=0.25, z=0, planar=True),
										transitions={'done': 'log app', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pos', 'pose_out': 'approach_pose'})

			# x:847 y:643
			OperatableStateMachine.add('ReturnApproachPose',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'ReturnPreGrip', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'approach_pose'})

			# x:1057 y:638
			OperatableStateMachine.add('ReturnPreGrip',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'PreGripPose'})

			# x:152 y:107
			OperatableStateMachine.add('LOG POSE',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'MoveIt_isReachable'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'pos'})

			# x:134 y:474
			OperatableStateMachine.add('log app',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Move_approach'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'approach_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
