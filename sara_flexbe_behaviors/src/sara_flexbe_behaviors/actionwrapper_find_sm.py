#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_behaviors.action_find_sm import Action_findSM as sara_flexbe_behaviors__Action_findSM
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 30/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_FindSM(Behavior):
	'''
	Action Wrapper for find an object visually arround the robot.
	'''


	def __init__(self):
		super(ActionWrapper_FindSM, self).__init__()
		self.name = 'ActionWrapper_Find'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_findSM, 'Action_find')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1498 67 
		# Find|n1- what to find|n2- where to look for



	def create(self):
		# x:711 y:84, x:836 y:453, x:709 y:633
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Find","cup"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:67 y:70
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] is not None and x[1] != ''),
										transitions={'true': 'ReadParameters', 'false': 'say no object given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:325 y:70
			OperatableStateMachine.add('say no object given',
										SaraSay(sentence="You didn't told me what to find.", emotion=1, block=True),
										transitions={'done': 'Cause1'},
										autonomy={'done': Autonomy.Off})

			# x:75 y:253
			OperatableStateMachine.add('say find object',
										SaraSayKey(Format=lambda x: "I'm now looking for the " + x, emotion=1, block=True),
										transitions={'done': 'Action_find'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:68 y:363
			OperatableStateMachine.add('Action_find',
										self.use_behavior(sara_flexbe_behaviors__Action_findSM, 'Action_find'),
										transitions={'done': 'Say Finded Object', 'failed': 'SayNotFound'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'name', 'entity': 'entity'})

			# x:77 y:159
			OperatableStateMachine.add('ReadParameters',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'say find object'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:235 y:150
			OperatableStateMachine.add('Say Finded Object',
										SaraSayKey(Format=lambda x: "I just find the " + x.name, emotion=1, block=True),
										transitions={'done': 'Get Time'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'entity'})

			# x:357 y:269
			OperatableStateMachine.add('Get Time',
										CalculationState(calculation=lambda x: x.lastUpdateTime.secs),
										transitions={'done': 'Get Id'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'currentTime'})

			# x:405 y:146
			OperatableStateMachine.add('Get Id',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Set Time'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'id'})

			# x:490 y:316
			OperatableStateMachine.add('Set Time',
										SetRosParam(ParamName="/behavior/FoundEntity/lastUpdate"),
										transitions={'done': 'Set Id'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'currentTime'})

			# x:645 y:323
			OperatableStateMachine.add('Set Id',
										SetRosParam(ParamName="/behavior/FoundEntity/Id"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'id'})

			# x:267 y:369
			OperatableStateMachine.add('SayNotFound',
										SaraSayKey(Format=lambda x: "I did not find the " + x + ".", emotion=1, block=True),
										transitions={'done': 'cause2'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:835 y:14
			OperatableStateMachine.add('Cause1',
										SetKey(Value="You didn't told me what to find."),
										transitions={'done': 'set cause in rosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:646 y:460
			OperatableStateMachine.add('cause2',
										SetKey(Value="I didn't find the object"),
										transitions={'done': 'set cause in rosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:769 y:347
			OperatableStateMachine.add('set cause in rosparam',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
