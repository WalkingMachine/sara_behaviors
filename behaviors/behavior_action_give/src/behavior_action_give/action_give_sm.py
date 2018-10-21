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
from flexbe_states.log_state import LogState
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.sara_follow import SaraFollow
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.calculation_state import CalculationState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1195 y:433, x:121 y:572, x:572 y:82, x:1118 y:593
		_state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'No_object_in_hand', 'fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:130 y:365
		_sm_lookat_0 = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])

		with _sm_lookat_0:
			# x:114 y:127
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'look'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:299 y:300, x:263 y:535
		_sm_give_1 = OperatableStateMachine(outcomes=['failed', 'given'], input_keys=['Object'])

		with _sm_give_1:
			# x:67 y:27
			OperatableStateMachine.add('SetPose',
										SetKey(Value="ShowGripper"),
										transitions={'done': 'say give'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:53 y:413
			OperatableStateMachine.add('read torque',
										ReadTorque(watchdog=5, Joint="right_elbow_pitch_joint", Threshold=2, min_time=1),
										transitions={'threshold': 'open gripper', 'watchdog': 'read torque', 'fail': 'failed'},
										autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'torque': 'torque'})

			# x:52 y:500
			OperatableStateMachine.add('open gripper',
										SetGripperState(width=0.15, effort=1),
										transitions={'object': 'given', 'no_object': 'given'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:62 y:99
			OperatableStateMachine.add('say give',
										SaraSayKey(Format=lambda x: "Hi. I'm giving you this "+str(x), emotion=1, block=False),
										transitions={'done': 'moveArm'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Object'})

			# x:64 y:248
			OperatableStateMachine.add('say pull',
										SaraSay(sentence="You can pull on it", emotion=1, block=False),
										transitions={'done': 'wait 1'},
										autonomy={'done': Autonomy.Off})

			# x:64 y:325
			OperatableStateMachine.add('wait 1',
										WaitState(wait_time=1),
										transitions={'done': 'read torque'},
										autonomy={'done': Autonomy.Off})

			# x:57 y:175
			OperatableStateMachine.add('moveArm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say pull', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})


		# x:596 y:480
		_sm_follow_2 = OperatableStateMachine(outcomes=['finished'], input_keys=['ID'])

		with _sm_follow_2:
			# x:180 y:123
			OperatableStateMachine.add('follow',
										SaraFollow(distance=1.5, ReplanPeriod=0.5),
										transitions={'failed': 'follow'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:313 y:247, x:301 y:177, x:103 y:293, x:343 y:113, x:397 y:411, x:311 y:27, x:630 y:365, x:730 y:365
		_sm_give_3 = ConcurrencyContainer(outcomes=['failed', 'given', 'continue'], input_keys=['ID', 'Object'], conditions=[
										('failed', [('Give', 'failed')]),
										('given', [('Give', 'given')]),
										('given', [('Follow', 'finished')]),
										('failed', [('LookAt', 'failed')])
										])

		with _sm_give_3:
			# x:91 y:50
			OperatableStateMachine.add('Follow',
										_sm_follow_2,
										transitions={'finished': 'given'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:84 y:164
			OperatableStateMachine.add('Give',
										_sm_give_1,
										transitions={'failed': 'failed', 'given': 'given'},
										autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit},
										remapping={'Object': 'Object'})

			# x:175 y:371
			OperatableStateMachine.add('LookAt',
										_sm_lookat_0,
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:77 y:29
			OperatableStateMachine.add('Get hand contaent',
										GetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'is object in hand?', 'failed': 'fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'Object'})

			# x:75 y:113
			OperatableStateMachine.add('is object in hand?',
										CheckConditionState(predicate=lambda x: x),
										transitions={'true': 'name', 'false': 'log empty hand'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Object'})

			# x:70 y:277
			OperatableStateMachine.add('list persons',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'get id', 'none_found': 'Person_not_found'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'People_list', 'number': 'number'})

			# x:434 y:62
			OperatableStateMachine.add('log empty hand',
										LogState(text="The hand is empty. Set the GripperContent rosParam", severity=Logger.REPORT_HINT),
										transitions={'done': 'No_object_in_hand'},
										autonomy={'done': Autonomy.Off})

			# x:971 y:298
			OperatableStateMachine.add('log moveitfail',
										LogState(text="moveit failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'fail'},
										autonomy={'done': Autonomy.Off})

			# x:815 y:527
			OperatableStateMachine.add('log movebase fail',
										LogState(text="giving Failed", severity=Logger.REPORT_HINT),
										transitions={'done': 'fail'},
										autonomy={'done': Autonomy.Off})

			# x:863 y:76
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

			# x:515 y:515
			OperatableStateMachine.add('give',
										_sm_give_3,
										transitions={'failed': 'log movebase fail', 'given': 'set idle pose', 'continue': 'give'},
										autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit, 'continue': Autonomy.Inherit},
										remapping={'ID': 'ID', 'Object': 'Object'})

			# x:256 y:278
			OperatableStateMachine.add('get id',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'give'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'People_list', 'output_value': 'ID'})

			# x:95 y:195
			OperatableStateMachine.add('name',
										SetKey(Value="person"),
										transitions={'done': 'list persons'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
