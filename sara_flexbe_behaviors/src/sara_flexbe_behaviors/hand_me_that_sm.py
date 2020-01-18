#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.GetPointedPositionOnPlane import GetPointedPositionOnPlane
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_behaviors.action_point_at_sm import Action_point_atSM as sara_flexbe_behaviors__Action_point_atSM
from sara_flexbe_states.LookAtPos import LookAtPos
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jan 18 2020
@author: Huynh-Anh Le
'''
class Hand_me_thatSM(Behavior):
	'''
	Robot identifies object pointed by an operator
	'''


	def __init__(self):
		super(Hand_me_thatSM, self).__init__()
		self.name = 'Hand_me_that'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_point_atSM, 'ReceiveQuestion/lookObject/DesignatedObject/points at it/Action_point_at')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:492 y:377, x:577 y:309
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_looks_at_it_0 = OperatableStateMachine(outcomes=['fail'], input_keys=['position'])

		with _sm_looks_at_it_0:
			# x:126 y:99
			OperatableStateMachine.add('look',
										LookAtPos(),
										transitions={'failed': 'look', 'done': 'look'},
										autonomy={'failed': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'pos': 'position'})


		# x:30 y:365
		_sm_points_at_it_1 = OperatableStateMachine(outcomes=['finished'], input_keys=['position'])

		with _sm_points_at_it_1:
			# x:112 y:202
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(sara_flexbe_behaviors__Action_point_atSM, 'ReceiveQuestion/lookObject/DesignatedObject/points at it/Action_point_at'),
										transitions={'finished': 'Action_point_at', 'failed': 'Action_point_at'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'position'})


		# x:30 y:365
		_sm_moves_to_it_2 = OperatableStateMachine(outcomes=['arrived'], input_keys=['position'])

		with _sm_moves_to_it_2:
			# x:204 y:52
			OperatableStateMachine.add('set distance',
										SetKey(Value=1),
										transitions={'done': 'get pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:211 y:185
			OperatableStateMachine.add('get pose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'move to bag'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'pose'})

			# x:188 y:279
			OperatableStateMachine.add('move to bag',
										SaraMoveBase(reference="map"),
										transitions={'arrived': 'arrived', 'failed': 'arrived'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_designatedobject_3 = ConcurrencyContainer(outcomes=['finished'], input_keys=['position'], conditions=[
										('finished', [('looks at it', 'fail')]),
										('finished', [('points at it', 'finished')]),
										('finished', [('moves to it', 'arrived')])
										])

		with _sm_designatedobject_3:
			# x:499 y:118
			OperatableStateMachine.add('moves to it',
										_sm_moves_to_it_2,
										transitions={'arrived': 'finished'},
										autonomy={'arrived': Autonomy.Inherit},
										remapping={'position': 'position'})

			# x:239 y:126
			OperatableStateMachine.add('points at it',
										_sm_points_at_it_1,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'position': 'position'})

			# x:45 y:121
			OperatableStateMachine.add('looks at it',
										_sm_looks_at_it_0,
										transitions={'fail': 'finished'},
										autonomy={'fail': Autonomy.Inherit},
										remapping={'position': 'position'})


		# x:30 y:365
		_sm_lookeyes_4 = OperatableStateMachine(outcomes=['finished'])

		with _sm_lookeyes_4:
			# x:189 y:48
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=3),
										transitions={'done': 'say ready'},
										autonomy={'done': Autonomy.Off})

			# x:171 y:288
			OperatableStateMachine.add('reset head',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:164 y:163
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="Good, I see you want this bag. But, could you hand it to me please?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'reset head'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:322
		_sm_lookobject_5 = OperatableStateMachine(outcomes=['finished'])

		with _sm_lookobject_5:
			# x:35 y:70
			OperatableStateMachine.add('setName',
										SetKey(Value="person"),
										transitions={'done': 'say 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personName'})

			# x:233 y:109
			OperatableStateMachine.add('say 1',
										SaraSay(sentence="Please, tell me what you need", input_keys=[], emotion=0, block=True),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:193
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'calculation', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'personName', 'entity_list': 'entity_list', 'number': 'number'})

			# x:230 y:363
			OperatableStateMachine.add('GetObjectPointing',
										GetPointedPositionOnPlane(planeHeight=0.2),
										transitions={'done': 'DesignatedObject', 'not_pointing': 'say 1', 'pointing_up': 'say 1', 'failed': 'list'},
										autonomy={'done': Autonomy.Off, 'not_pointing': Autonomy.Off, 'pointing_up': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entity': 'entity', 'position': 'position'})

			# x:34 y:362
			OperatableStateMachine.add('calculation',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetObjectPointing'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})

			# x:241 y:554
			OperatableStateMachine.add('DesignatedObject',
										_sm_designatedobject_3,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'position': 'position'})


		# x:93 y:398, x:227 y:405
		_sm_receivequestion_6 = OperatableStateMachine(outcomes=['failed', 'done'])

		with _sm_receivequestion_6:
			# x:66 y:44
			OperatableStateMachine.add('lookObject',
										_sm_lookobject_5,
										transitions={'finished': 'close'},
										autonomy={'finished': Autonomy.Inherit})

			# x:81 y:157
			OperatableStateMachine.add('close',
										SetGripperState(width=0, effort=0),
										transitions={'object': 'LookEyes', 'no_object': 'LookEyes'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:75 y:265
			OperatableStateMachine.add('LookEyes',
										_sm_lookeyes_4,
										transitions={'finished': 'done'},
										autonomy={'finished': Autonomy.Inherit})



		with _state_machine:
			# x:67 y:48
			OperatableStateMachine.add('start',
										ContinueButton(),
										transitions={'true': 'ReceiveQuestion', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:229 y:139
			OperatableStateMachine.add('ReceiveQuestion',
										_sm_receivequestion_6,
										transitions={'failed': 'failed', 'done': 'finished'},
										autonomy={'failed': Autonomy.Inherit, 'done': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
