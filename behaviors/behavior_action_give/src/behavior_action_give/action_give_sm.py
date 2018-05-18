#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.SetKey import SetKey
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.set_gripper_state import SetGripperState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class Action_GiveSM(Behavior):
	'''
	give the content of the gripper to a person.
	'''


	def __init__(self):
		super(Action_GiveSM, self).__init__()
		self.name = 'Action_Give'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:738 y:144, x:122 y:501, x:352 y:119, x:744 y:253
		_state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'No_object_in_hand', 'fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:29
			OperatableStateMachine.add('Get hand contaent',
										GetRosParam(ParamName="GripperContent"),
										transitions={'done': 'is object in hand?', 'failed': 'No_object_in_hand'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Object'})

			# x:75 y:113
			OperatableStateMachine.add('is object in hand?',
										CheckConditionState(predicate=lambda x: x),
										transitions={'true': 'list persons', 'false': 'No_object_in_hand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Object'})

			# x:76 y:202
			OperatableStateMachine.add('list persons',
										list_entities_by_name(Name="person", frontality_level=0.5),
										transitions={'found': 'get closest', 'not_found': 'Person_not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'Entities_list': 'Entities_list', 'number': 'number'})

			# x:310 y:205
			OperatableStateMachine.add('get closest',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetPos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entities_list', 'output_value': 'Person'})

			# x:293 y:436
			OperatableStateMachine.add('GenPose',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Not rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'Position', 'distance': 'distance', 'pose_out': 'Pose'})

			# x:312 y:286
			OperatableStateMachine.add('GetPos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'set distance'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Person', 'output_value': 'Position'})

			# x:316 y:361
			OperatableStateMachine.add('set distance',
										SetKey(Value=1.5),
										transitions={'done': 'GenPose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:476 y:505
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'SetPose', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'Pose', 'relative': 'relative'})

			# x:330 y:516
			OperatableStateMachine.add('Not rel',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:495 y:329
			OperatableStateMachine.add('moveArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'read torque', 'failed': 'fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:504 y:409
			OperatableStateMachine.add('SetPose',
										SetKey(Value="GivePos"),
										transitions={'done': 'moveArm'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:494 y:244
			OperatableStateMachine.add('read torque',
										ReadTorque(watchdog=5, Joint="right_elbow_pitch_joint", Threshold=0.01, min_time=1),
										transitions={'threshold': 'open gripper', 'watchdog': 'open gripper', 'fail': 'fail'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:486 y:139
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'Given', 'no_object': 'Given'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
