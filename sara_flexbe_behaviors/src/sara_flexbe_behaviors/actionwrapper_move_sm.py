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
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.SetRosParam import SetRosParam
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 22/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_MoveSM(Behavior):
	'''
	action wrapper pour move
	'''


	def __init__(self):
		super(ActionWrapper_MoveSM, self).__init__()
		self.name = 'ActionWrapper_Move'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Try to reach/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 290 19 
		# Move|n1- Location|n2- Location Container|n3- Location Container



	def create(self):
		# x:267 y:194, x:706 y:131, x:92 y:292
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Move",'crowd']
		_state_machine.userdata.relative = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:131 y:459, x:447 y:470
		_sm_try_to_reach_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])

		with _sm_try_to_reach_0:
			# x:84 y:67
			OperatableStateMachine.add('get destination',
										CalculationState(calculation=lambda x: x[1:]),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'destination'})

			# x:258 y:149
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Try to reach/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'destination', 'relative': 'destination'})



		with _state_machine:
			# x:65 y:108
			OperatableStateMachine.add('Try to reach',
										_sm_try_to_reach_0,
										transitions={'finished': 'finished', 'failed': 'gen fail cause'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:532 y:113
			OperatableStateMachine.add('paramoffailure',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'FailureCause'})

			# x:290 y:110
			OperatableStateMachine.add('gen fail cause',
										CalculationState(calculation=lambda x: "I couldn't reach the "+x[1]+"."),
										transitions={'done': 'paramoffailure'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'FailureCause'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
