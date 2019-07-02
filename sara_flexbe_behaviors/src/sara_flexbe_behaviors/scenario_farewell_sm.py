#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_behaviors.farewell_sm import FarewellSM as sara_flexbe_behaviors__FarewellSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jun 16 2019
@author: Huynh-Anh Le
'''
class Scenario_FarewellSM(Behavior):
	'''
	Scenario farewell
	'''


	def __init__(self):
		super(Scenario_FarewellSM, self).__init__()
		self.name = 'Scenario_Farewell'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__FarewellSM, 'Farewell_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move')
		self.add_behavior(sara_flexbe_behaviors__FarewellSM, 'Farewell')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1244 y:151, x:1069 y:298
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:18 y:27
			OperatableStateMachine.add('GetOrigin',
										Get_Robot_Pose(),
										transitions={'done': 'Farewell'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'poseOrigin'})

			# x:648 y:109
			OperatableStateMachine.add('Farewell_2',
										self.use_behavior(sara_flexbe_behaviors__FarewellSM, 'Farewell_2'),
										transitions={'finished': 'finish', 'failed': 'didnt succed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:287 y:199
			OperatableStateMachine.add('Try again',
										SaraSay(sentence="I will try with the next person", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:348 y:30
			OperatableStateMachine.add('say next',
										SaraSay(sentence="I will now get the net person.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off})

			# x:449 y:113
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'Farewell_2', 'failed': 'Action_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'poseOrigin'})

			# x:801 y:37
			OperatableStateMachine.add('finish',
										SaraSay(sentence="I am done BYe bye", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move_2'},
										autonomy={'done': Autonomy.Off})

			# x:771 y:211
			OperatableStateMachine.add('didnt succed',
										SaraSay(sentence="I failed sorry", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_Move_2'},
										autonomy={'done': Autonomy.Off})

			# x:157 y:74
			OperatableStateMachine.add('Farewell',
										self.use_behavior(sara_flexbe_behaviors__FarewellSM, 'Farewell'),
										transitions={'finished': 'say next', 'failed': 'Try again'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:982 y:154
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'poseOrigin'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
