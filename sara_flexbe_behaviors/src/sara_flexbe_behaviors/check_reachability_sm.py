#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.moveit_move import MoveitMove
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Check_reachabilitySM(Behavior):
	'''
	check if the object is in range
	'''


	def __init__(self):
		super(Check_reachabilitySM, self).__init__()
		self.name = 'Check_reachability'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:609 y:365, x:602 y:89
		_state_machine = OperatableStateMachine(outcomes=['ok', 'too_far'], input_keys=['pose'])
		_state_machine.userdata.pose = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:42 y:56
			OperatableStateMachine.add('gen',
										GenGripperPose(l=0, z=0, planar=false),
										transitions={'done': 'kinematic test', 'fail': 'too_far'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

			# x:195 y:347
			OperatableStateMachine.add('third check',
										CheckConditionState(predicate=lambda x: (x.position.x**2+x.position.y**2+(x.position.z-1))**0.5 < 1.5),
										transitions={'true': 'kinematic test', 'false': 'too_far'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'pose_out'})

			# x:190 y:147
			OperatableStateMachine.add('first check',
										CheckConditionState(predicate=lambda x: x.position.x<0.8),
										transitions={'true': 'second check', 'false': 'too_far'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'pose_out'})

			# x:196 y:253
			OperatableStateMachine.add('second check',
										CheckConditionState(predicate=lambda x: x.position.z>0.5),
										transitions={'true': 'third check', 'false': 'too_far'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'pose_out'})

			# x:99 y:520
			OperatableStateMachine.add('kinematic test',
										MoveitMove(move=False, waitForExecution=True, group="RightArm"),
										transitions={'done': 'ok', 'failed': 'too_far'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'pose_out'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
