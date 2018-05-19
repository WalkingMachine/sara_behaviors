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
from flexbe_states.log_state import LogState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.SetRosParam import SetRosParam
from flexbe_states.wait_state import WaitState
from behavior_action_point_at.action_point_at_sm import Action_point_atSM
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
		self.add_behavior(Action_point_atSM, 'Action_point_at')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1195 y:433, x:122 y:501, x:323 y:140, x:745 y:220
		_state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'No_object_in_hand', 'fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:77 y:29
			OperatableStateMachine.add('Get hand contaent',
										GetRosParam(ParamName="GripperContent"),
										transitions={'done': 'is object in hand?', 'failed': 'log empty hand'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Object'})

			# x:75 y:113
			OperatableStateMachine.add('is object in hand?',
										CheckConditionState(predicate=lambda x: x),
										transitions={'true': 'list persons', 'false': 'log empty hand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Object'})

			# x:76 y:202
			OperatableStateMachine.add('list persons',
										list_entities_by_name(Name="person", frontality_level=0.5),
										transitions={'found': 'get closest', 'not_found': 'Person_not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'Entities_list': 'People_list', 'number': 'number'})

			# x:310 y:205
			OperatableStateMachine.add('get closest',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'GetPos'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'People_list', 'output_value': 'Person'})

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
										transitions={'finished': 'SetPose', 'failed': 'log movebase fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'Pose', 'relative': 'relative'})

			# x:330 y:516
			OperatableStateMachine.add('Not rel',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:489 y:264
			OperatableStateMachine.add('moveArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say pull', 'failed': 'log moveitfail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:504 y:409
			OperatableStateMachine.add('SetPose',
										SetKey(Value="ShowGripper"),
										transitions={'done': 'say give'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:474 y:52
			OperatableStateMachine.add('read torque',
										ReadTorque(watchdog=5, Joint="right_shoulder_pitch_joint", Threshold=0.5, min_time=1),
										transitions={'threshold': 'open gripper', 'watchdog': 'open gripper', 'fail': 'fail'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:665 y:52
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'set idle pose', 'no_object': 'set idle pose'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:290 y:56
			OperatableStateMachine.add('log empty hand',
										LogState(text="The hand is empty. Set the GripperContent rosParma", severity=Logger.REPORT_HINT),
										transitions={'done': 'No_object_in_hand'},
										autonomy={'done': Autonomy.Off})

			# x:931 y:213
			OperatableStateMachine.add('log torque fail',
										LogState(text="torque reading failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'fail'},
										autonomy={'done': Autonomy.Off})

			# x:895 y:315
			OperatableStateMachine.add('log moveitfail',
										LogState(text="moveit failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'fail'},
										autonomy={'done': Autonomy.Off})

			# x:892 y:395
			OperatableStateMachine.add('log movebase fail',
										LogState(text="ActionMove Failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'fail'},
										autonomy={'done': Autonomy.Off})

			# x:856 y:60
			OperatableStateMachine.add('set idle pose',
										SetKey(Value="IdlePose"),
										transitions={'done': 'say good'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:1174 y:94
			OperatableStateMachine.add('moveArm2',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'set none', 'failed': 'log moveitfail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:494 y:336
			OperatableStateMachine.add('say give',
										SaraSayKey(Format=lambda x: "Hi. I'm giving you this "+str(x), emotion=1, block=False),
										transitions={'done': 'Action_point_at'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Object'})

			# x:488 y:183
			OperatableStateMachine.add('say pull',
										SaraSay(sentence="You can pull on it", emotion=1, block=False),
										transitions={'done': 'wait 1'},
										autonomy={'done': Autonomy.Off})

			# x:1012 y:76
			OperatableStateMachine.add('say good',
										SaraSayKey(Format=lambda x: "Good, enjoy your "+str(x), emotion=1, block=True),
										transitions={'done': 'moveArm2'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Object'})

			# x:1167 y:337
			OperatableStateMachine.add('close gripper',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'Given', 'no_object': 'Given'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:1258 y:255
			OperatableStateMachine.add('remove gripper content',
										SetRosParam(ParamName="GripperContent"),
										transitions={'done': 'close gripper'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'none'})

			# x:1180 y:179
			OperatableStateMachine.add('set none',
										SetKey(Value=None),
										transitions={'done': 'close gripper'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'none'})

			# x:486 y:115
			OperatableStateMachine.add('wait 1',
										WaitState(wait_time=1),
										transitions={'done': 'read torque'},
										autonomy={'done': Autonomy.Off})

			# x:612 y:347
			OperatableStateMachine.add('Action_point_at',
										self.use_behavior(Action_point_atSM, 'Action_point_at'),
										transitions={'finished': 'say pull', 'failed': 'log moveitfail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'targetPoint': 'Position'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
