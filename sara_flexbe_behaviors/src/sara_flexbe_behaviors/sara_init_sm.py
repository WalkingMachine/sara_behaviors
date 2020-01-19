#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Mar 18 2019
@author: Huynh-Anh Le
'''
class Sara_InitSM(Behavior):
	'''
	Initialise la tete, le bras de Sara
	'''


	def __init__(self):
		super(Sara_InitSM, self).__init__()
		self.name = 'Sara_Init'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:123 y:357, x:288 y:339
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose_Init = "IdlePose"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:42 y:58
			OperatableStateMachine.add('Hi',
										SaraSay(sentence="Hi, my name is Sara and I will start", input_keys=[], emotion=0, block=True),
										transitions={'done': 'setHead'},
										autonomy={'done': Autonomy.Off})

			# x:77 y:210
			OperatableStateMachine.add('SetArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm", watchdog=15),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Pose_Init'})

			# x:72 y:130
			OperatableStateMachine.add('setHead',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'SetArm'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
