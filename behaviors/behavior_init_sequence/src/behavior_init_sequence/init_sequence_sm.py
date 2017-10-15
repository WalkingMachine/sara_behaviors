#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_init_sequence')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.pose_gen_quat import GenPoseQuat
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
		# x:976 y:64, x:579 y:148
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:113 y:34
			OperatableStateMachine.add('Wait_to_begin',
										WaitState(wait_time=10),
										transitions={'done': 'Gen_Pose_First_Objectif'},
										autonomy={'done': Autonomy.Off})

			# x:731 y:51
			OperatableStateMachine.add('Go_To_First_Objectif',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:418 y:50
			OperatableStateMachine.add('Gen_Pose_First_Objectif',
										GenPoseQuat(x=4.9627, y=-0.62033, z=0, ox=0, oy=0, oz=0.9125315, ow=-0.4090063),
										transitions={'done': 'Go_To_First_Objectif', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
