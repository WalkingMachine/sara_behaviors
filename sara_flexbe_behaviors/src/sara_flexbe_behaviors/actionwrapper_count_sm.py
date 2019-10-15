#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_behaviors.action_count_sm import Action_countSM as Action_countSM
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.SetRosParamKey import SetRosParamKey
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 27 2018
@author: Philippe La Madeleine
'''
class ActionWrapper_CountSM(Behavior):
	'''
	Count something
	'''


	def __init__(self):
		super(ActionWrapper_CountSM, self).__init__()
		self.name = 'ActionWrapper_Count'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_countSM, 'Action_count')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 282 30 
		# ["Count", "objects_name", "value_name"]



	def create(self):
		# x:254 y:640, x:565 y:232, x:530 y:448
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Count", "bottle", "behavior/Count/CountedObject"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:41 y:32
			OperatableStateMachine.add('get name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Say_Start'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'className'})

			# x:22 y:213
			OperatableStateMachine.add('Action_count',
										self.use_behavior(Action_countSM, 'Action_count'),
										transitions={'done': 'get paramname', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'className', 'Count': 'Count'})

			# x:14 y:462
			OperatableStateMachine.add('concat',
										FlexibleCalculationState(calculation=lambda x: "I counted "+str(x[0])+" "+str(x[1])+".", input_keys=["Count", "className"]),
										transitions={'done': 'Say_Count'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'className': 'className', 'output_value': 'sentence'})

			# x:28 y:388
			OperatableStateMachine.add('store param',
										SetRosParamKey(),
										transitions={'done': 'concat'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Count', 'ParamName': 'ParamName'})

			# x:45 y:290
			OperatableStateMachine.add('get paramname',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'store param'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'ParamName'})

			# x:17 y:633
			OperatableStateMachine.add('set head back',
										SaraSetHeadAngle(pitch=-0.3, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:36 y:120
			OperatableStateMachine.add('Say_Start',
										SaraSay(sentence=lambda x: "I'm starting to count the "+str(x)+"s.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'Action_count'},
										autonomy={'done': Autonomy.Off})

			# x:27 y:546
			OperatableStateMachine.add('Say_Count',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'set head back'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
