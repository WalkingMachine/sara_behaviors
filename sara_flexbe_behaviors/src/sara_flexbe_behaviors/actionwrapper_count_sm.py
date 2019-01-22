#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_count')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from behavior_action_count.action_count_sm import Action_countSM
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.SetRosParamKey import SetRosParamKey
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
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
										transitions={'done': 'say start'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'className'})

			# x:13 y:220
			OperatableStateMachine.add('Action_count',
										self.use_behavior(Action_countSM, 'Action_count'),
										transitions={'done': 'get paramname', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'className', 'Count': 'Count'})

			# x:14 y:473
			OperatableStateMachine.add('concat',
										FlexibleCalculationState(calculation=lambda x: "I counted "+str(x[0])+" "+str(x[1])+".", input_keys=["Count", "className"]),
										transitions={'done': 'say count'},
										autonomy={'done': Autonomy.Off},
										remapping={'Count': 'Count', 'className': 'className', 'output_value': 'sentence'})

			# x:24 y:554
			OperatableStateMachine.add('say count',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'set head back'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'sentence'})

			# x:17 y:394
			OperatableStateMachine.add('store param',
										SetRosParamKey(),
										transitions={'done': 'concat'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Count', 'ParamName': 'ParamName'})

			# x:20 y:312
			OperatableStateMachine.add('get paramname',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'store param'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'ParamName'})

			# x:41 y:125
			OperatableStateMachine.add('say start',
										SaraSayKey(Format=lambda x: "I'm starting to count the "+str(x)+"s.", emotion=1, block=False),
										transitions={'done': 'Action_count'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'className'})

			# x:17 y:633
			OperatableStateMachine.add('set head back',
										SaraSetHeadAngle(pitch=-0.3, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
