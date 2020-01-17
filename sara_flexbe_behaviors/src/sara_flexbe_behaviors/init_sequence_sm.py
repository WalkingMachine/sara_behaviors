#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.run_trajectory import RunTrajectory
from sara_flexbe_states.set_gripper_state import SetGripperState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 27 2017
@author: Redouane Laref Nicolas Nadeau
'''
class Init_SequenceSM(Behavior):
	'''
	Initialisation Sequence
	'''


	def __init__(self):
		super(Init_SequenceSM, self).__init__()
		self.name = 'Init_Sequence'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:976 y:64, x:973 y:289
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:42 y:72
			OperatableStateMachine.add('INIT HEAD',
										SaraSetHeadAngle(pitch=0.4, yaw=0),
										transitions={'done': 'repos'},
										autonomy={'done': Autonomy.Off})

			# x:205 y:72
			OperatableStateMachine.add('repos',
										RunTrajectory(file="repos", duration=0),
										transitions={'done': 'opengrip'},
										autonomy={'done': Autonomy.Off})

			# x:506 y:86
			OperatableStateMachine.add('opengrip',
										SetGripperState(width=0.1, effort=0),
										transitions={'object': 'finished', 'no_object': 'finished'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
