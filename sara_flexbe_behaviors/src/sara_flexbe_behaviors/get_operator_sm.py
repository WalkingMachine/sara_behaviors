#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 09 2018
@author: Philippe La Madeleine
'''
class Get_operatorSM(Behavior):
	'''
	Find an person and ask them to become operator
	'''


	def __init__(self):
		super(Get_operatorSM, self).__init__()
		self.name = 'Get_operator'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Move to person/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:814 y:45, x:514 y:274
		_state_machine = OperatableStateMachine(outcomes=['Found', 'NotFound'], output_keys=['Operator'])
		_state_machine.userdata.Operator = None
		_state_machine.userdata.Name = "person"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:506 y:393, x:515 y:462
		_sm_move_to_person_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Operator'])

		with _sm_move_to_person_0:
			# x:30 y:83
			OperatableStateMachine.add('Getpos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'setDistance'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Operator', 'output_value': 'pose_in'})

			# x:35 y:450
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Move to person/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'Pose'})

			# x:47 y:368
			OperatableStateMachine.add('set not rel',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:41 y:179
			OperatableStateMachine.add('setDistance',
										SetKey(Value=1.5),
										transitions={'done': 'Close position'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:27 y:280
			OperatableStateMachine.add('Close position',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'set not rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'pose_in', 'distance': 'distance', 'pose_out': 'Pose'})



		with _state_machine:
			# x:64 y:35
			OperatableStateMachine.add('Get previous ID',
										GetRosParam(ParamName="behavior/Operator/Id"),
										transitions={'done': 'Get Operator', 'failed': 'for 3'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:271 y:37
			OperatableStateMachine.add('Get Operator',
										GetEntityByID(),
										transitions={'found': 'Found', 'not_found': 'Say lost operator'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Operator'})

			# x:263 y:155
			OperatableStateMachine.add('Say lost operator',
										SaraSay(sentence="I lost my operator", input_keys=[], emotion=1, block=True),
										transitions={'done': 'for 3'},
										autonomy={'done': Autonomy.Off})

			# x:780 y:517
			OperatableStateMachine.add('ask if operator',
										SaraSay(sentence="Are you my operator?", input_keys=[], emotion=1, block=True),
										transitions={'done': 'get speech'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:273
			OperatableStateMachine.add('for 3',
										ForLoop(repeat=3),
										transitions={'do': 'for 3_2', 'end': 'set None'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:249 y:357
			OperatableStateMachine.add('say where are you',
										SaraSay(sentence="Operator. Where are you?", input_keys=[], emotion=1, block=True),
										transitions={'done': 'for 3'},
										autonomy={'done': Autonomy.Off})

			# x:281 y:265
			OperatableStateMachine.add('set None',
										SetKey(Value=None),
										transitions={'done': 'NotFound'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Operator'})

			# x:49 y:511
			OperatableStateMachine.add('Get persons',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'get next closest', 'none_found': 'say where are you'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'Name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:461 y:475
			OperatableStateMachine.add('Move to person',
										_sm_move_to_person_0,
										transitions={'finished': 'ask if operator', 'failed': 'NotFound'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Operator': 'Operator'})

			# x:783 y:161
			OperatableStateMachine.add('set new ID',
										SetRosParam(ParamName="behavior/Operator/Id"),
										transitions={'done': 'Found'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:775 y:269
			OperatableStateMachine.add('get ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'set new ID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Operator', 'output_value': 'ID'})

			# x:784 y:433
			OperatableStateMachine.add('get speech',
										GetSpeech(watchdog=5),
										transitions={'done': 'Yes ?', 'nothing': 'for 3_2', 'fail': 'NotFound'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:69 y:402
			OperatableStateMachine.add('for 3_2',
										ForLoop(repeat=3),
										transitions={'do': 'Get persons', 'end': 'set None'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index2'})

			# x:744 y:332
			OperatableStateMachine.add('Yes ?',
										CheckConditionState(predicate=lambda x: "yes" in x),
										transitions={'true': 'get ID', 'false': 'for 3_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})

			# x:263 y:535
			OperatableStateMachine.add('get next closest',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["entity_list", "index"]),
										transitions={'done': 'ask if operator'},
										autonomy={'done': Autonomy.Off},
										remapping={'entity_list': 'entity_list', 'index': 'index', 'output_value': 'Operator'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
