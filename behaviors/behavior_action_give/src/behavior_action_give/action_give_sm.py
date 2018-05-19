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
from behavior_action_follow.action_follow_sm import Action_followSM
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
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
		self.add_behavior(Action_followSM, 'give/Action_follow')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1195 y:433, x:122 y:501, x:366 y:140, x:1118 y:593
		_state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'No_object_in_hand', 'fail'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:299 y:300, x:263 y:535
		_sm_give_0 = OperatableStateMachine(outcomes=['failed', 'given'], input_keys=['Object'])

		with _sm_give_0:
			# x:67 y:27
			OperatableStateMachine.add('SetPose',
										SetKey(Value="ShowGripper"),
										transitions={'done': 'say give'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:53 y:413
			OperatableStateMachine.add('read torque',
										ReadTorque(watchdog=5, Joint="right_shoulder_pitch_joint", Threshold=0.5, min_time=1),
										transitions={'threshold': 'open gripper', 'watchdog': 'open gripper', 'fail': 'failed'},
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


		# x:30 y:365, x:130 y:365, x:230 y:365, x:398 y:124, x:399 y:70, x:530 y:365, x:630 y:365
		_sm_give_1 = ConcurrencyContainer(outcomes=['failed', 'given', 'continue'], input_keys=['ID', 'Object'], conditions=[
										('failed', [('Give', 'failed')]),
										('given', [('Give', 'given')]),
										('continue', [('Action_follow', 'done')]),
										('failed', [('Action_follow', 'failed')])
										])

		with _sm_give_1:
			# x:95 y:66
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(Action_followSM, 'give/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:102 y:194
			OperatableStateMachine.add('Give',
										_sm_give_0,
										transitions={'failed': 'failed', 'given': 'given'},
										autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit},
										remapping={'Object': 'Object'})



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
										transitions={'found': 'get id', 'not_found': 'Person_not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'Entities_list': 'People_list', 'number': 'number'})

			# x:290 y:56
			OperatableStateMachine.add('log empty hand',
										LogState(text="The hand is empty. Set the GripperContent rosParma", severity=Logger.REPORT_HINT),
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
										_sm_give_1,
										transitions={'failed': 'log movebase fail', 'given': 'set idle pose', 'continue': 'give'},
										autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit, 'continue': Autonomy.Inherit},
										remapping={'ID': 'ID', 'Object': 'Object'})

			# x:251 y:205
			OperatableStateMachine.add('get id',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'give'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'People_list', 'output_value': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
