#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 14 2018
@author: Philippe La Madeleine
'''
class AGoHomeSM(Behavior):
	'''
	sara will go to her docking port
	'''


	def __init__(self):
		super(AGoHomeSM, self).__init__()
		self.name = 'A Go Home'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:57 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:40 y:96
			OperatableStateMachine.add('say home',
										SaraSay(sentence="I'm going back home.", input_keys=[], emotion=1, block=False),
										transitions={'done': 'gen origin'},
										autonomy={'done': Autonomy.Off})

			# x:41 y:338
			OperatableStateMachine.add('docked',
										SaraSay(sentence="Docking sequence initiated. Locking safety clamps. This robot will stay there as long as needed.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:238
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'docked', 'failed': 'Action_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose'})

			# x:32 y:160
			OperatableStateMachine.add('gen origin',
										GenPoseEuler(x=0, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
