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
from sara_flexbe_states.GetRosParamKey import GetRosParamKey
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 27 2018
@author: Philippe La Madeleine
'''
class ActionWrapper_SaySM(Behavior):
	'''
	Say something
	'''


	def __init__(self):
		super(ActionWrapper_SaySM, self).__init__()
		self.name = 'ActionWrapper_Say'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 165 22 
		# ["Say", "sentence"]



	def create(self):
		# x:783 y:268, x:448 y:352, x:564 y:354
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["say","coucou Philippe commit ca va"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:55 y:97
			OperatableStateMachine.add('calc',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'rosparamkey'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'sentence'})

			# x:271 y:123
			OperatableStateMachine.add('rosparamkey',
										GetRosParamKey(),
										transitions={'done': 'Sara_Speak', 'failed': 'Sara_Failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ParamName': 'sentence', 'Value': 'sentenceToSay'})

			# x:483 y:96
			OperatableStateMachine.add('Sara_Speak',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:473 y:212
			OperatableStateMachine.add('Sara_Failed',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
