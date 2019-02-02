#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.pose_gen_euler_key import GenPoseEulerKey
from sara_flexbe_states.sara_rel_move_base import SaraRelMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 21 2018
@author: Raphael Duchaine
'''
class action_turnSM(Behavior):
	'''
	Quality of life action

Ask for a rotation in degree with forward as 0deg

Verify which rotation is positive
	'''


	def __init__(self):
		super(action_turnSM, self).__init__()
		self.name = 'action_turn'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:622 y:0, x:619 y:113
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['rotation'])
		_state_machine.userdata.rotation = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:46 y:34
			OperatableStateMachine.add('setValue0',
										SetKey(Value=0),
										transitions={'done': 'GenPoseEulerKey'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'value0'})

			# x:194 y:46
			OperatableStateMachine.add('GenPoseEulerKey',
										GenPoseEulerKey(),
										transitions={'done': 'move'},
										autonomy={'done': Autonomy.Off},
										remapping={'xpos': 'value0', 'ypos': 'value0', 'zpos': 'value0', 'yaw': 'rotation', 'pitch': 'value0', 'roll': 'value0', 'pose': 'pose'})

			# x:356 y:30
			OperatableStateMachine.add('move',
										SaraRelMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
