#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.GenPointedPoints import GenPointedPoints
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.LookAtPos import LookAtPos
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.list_entities_near_point import list_entities_near_point
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class ATestSandboxSM(Behavior):
	'''
	Une behavior pour faire des tests rapidement.
	'''


	def __init__(self):
		super(ATestSandboxSM, self).__init__()
		self.name = 'A Test Sandbox'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:102 y:572, x:889 y:107
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.Pose1 = "PostGripPose"
		_state_machine.userdata.Pose2 = "IdlePose"
		_state_machine.userdata.actionList = [["Find", "bottle"], ["move", "kitchen"]]
		_state_machine.userdata.titre = "test"
		_state_machine.userdata.relative = False
		_state_machine.userdata.pitch = -0.8
		_state_machine.userdata.Action1 = ["move", "counter"]
		_state_machine.userdata.Action2 = ["move", "table"]
		_state_machine.userdata.pose = "Dining room"
		_state_machine.userdata.say1 = "say one"
		_state_machine.userdata.say2 = "say two"
		_state_machine.userdata.index = -1
		_state_machine.userdata.name = "person"
		_state_machine.userdata.name2 = "apple"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:28 y:104
			OperatableStateMachine.add('set_2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off})

			# x:190 y:78
			OperatableStateMachine.add('calc',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'gen'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'entity'})

			# x:351 y:116
			OperatableStateMachine.add('gen',
										GenPointedPoints(step=0.3, qty=5),
										transitions={'done': 'loop', 'not_pointing': 'say 1', 'failed': 'say2'},
										autonomy={'done': Autonomy.Off, 'not_pointing': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entity': 'entity', 'positionList': 'positionList'})

			# x:218 y:246
			OperatableStateMachine.add('loop',
										ForLoop(repeat=5),
										transitions={'do': 'flex calc', 'end': 'say 5'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:493 y:35
			OperatableStateMachine.add('say 1',
										SaraSay(sentence="Point at something", input_keys=[], emotion=0, block=True),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off})

			# x:533 y:125
			OperatableStateMachine.add('say2',
										SaraSay(sentence="Failed to generate points", input_keys=[], emotion=0, block=True),
										transitions={'done': 'list'},
										autonomy={'done': Autonomy.Off})

			# x:377 y:255
			OperatableStateMachine.add('flex calc',
										FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=["positionList","index"]),
										transitions={'done': 'look'},
										autonomy={'done': Autonomy.Off},
										remapping={'positionList': 'positionList', 'index': 'index', 'output_value': 'point'})

			# x:554 y:251
			OperatableStateMachine.add('look',
										LookAtPos(),
										transitions={'failed': 'say 3', 'done': 'list entities'},
										autonomy={'failed': Autonomy.Off, 'done': Autonomy.Off},
										remapping={'pos': 'point'})

			# x:403 y:354
			OperatableStateMachine.add('say 3',
										SaraSay(sentence="I can not look at this point", input_keys=[], emotion=0, block=True),
										transitions={'done': 'loop'},
										autonomy={'done': Autonomy.Off})

			# x:116 y:405
			OperatableStateMachine.add('say 5',
										SaraSay(sentence="I didn't see anything", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set'},
										autonomy={'done': Autonomy.Off})

			# x:150 y:493
			OperatableStateMachine.add('set',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:40
			OperatableStateMachine.add('list',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'calc', 'none_found': 'list'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:698 y:310
			OperatableStateMachine.add('list entities',
										list_entities_near_point(radius=2.0),
										transitions={'found': 'say 4', 'none_found': 'wait'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name2', 'position': 'point', 'entity_list': 'found_entity_list', 'number': 'number'})

			# x:714 y:407
			OperatableStateMachine.add('say 4',
										SaraSay(sentence="I see something.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set'},
										autonomy={'done': Autonomy.Off})

			# x:569 y:346
			OperatableStateMachine.add('wait',
										WaitState(wait_time=3),
										transitions={'done': 'loop'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
