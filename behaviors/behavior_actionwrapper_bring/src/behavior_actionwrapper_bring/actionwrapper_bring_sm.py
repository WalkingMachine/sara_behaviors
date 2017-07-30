#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_bring')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
from behavior_go_to_room.go_to_room_sm import Go_To_RoomSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_BringSM(Behavior):
	'''
	action wrapper pour bring
	'''


	def __init__(self):
		super(ActionWrapper_BringSM, self).__init__()
		self.name = 'ActionWrapper_Bring'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Go_To_RoomSM, 'Go_To_Room')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 508 30 
		# Bring|n1- object|n2- area|n3- beneficiary



	def create(self):
		# x:868 y:291, x:857 y:562
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action', 'index'])
		_state_machine.userdata.Action = ["Bring","love","the world"]
		_state_machine.userdata.index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:24 y:30
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'cond2', 'false': 'say no object given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:266 y:85
			OperatableStateMachine.add('say no object given',
										SaraSay(sentence="You didn't told me what to bring", emotion=1),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:176
			OperatableStateMachine.add('cond2',
										CheckConditionState(predicate=lambda x: x[2] != ''),
										transitions={'true': 'say3', 'false': 'say22'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:84 y:485
			OperatableStateMachine.add('say3',
										SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1]+" to "+x[2], emotion=1),
										transitions={'done': 'callculate name'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:133 y:279
			OperatableStateMachine.add('say22',
										SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1], emotion=1),
										transitions={'done': 'callculate name'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:354 y:321
			OperatableStateMachine.add('callculate name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Go_To_Room'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:567 y:335
			OperatableStateMachine.add('Go_To_Room',
										self.use_behavior(Go_To_RoomSM, 'Go_To_Room'),
										transitions={'finished': 'Go_To_Room', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'name': 'name', 'index': 'index'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
