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
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.Wonderland_Get_Object import WonderlandGetObject
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.moveit_move import MoveitMove
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from sara_flexbe_states.Wonderland_Get_Room import WonderlandGetRoom
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
		self.add_behavior(Action_MoveSM, 'Bring/Move_to_Object')
		self.add_behavior(Action_MoveSM, 'Bring/Move_Back')
		self.add_behavior(Action_MoveSM, 'Bring/Move_Forward')
		self.add_behavior(Action_pickSM, 'Bring/Action_pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 598 14 
		# Bring|n1- object|n2- area|n3- beneficiary



	def create(self):
		# x:868 y:291, x:857 y:562
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Bring","cup", "living room",""]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:529 y:68, x:662 y:494
		_sm_giving_back_0 = OperatableStateMachine(outcomes=['fail', 'done'], input_keys=['name'])

		with _sm_giving_back_0:
			# x:42 y:31
			OperatableStateMachine.add('setTarget',
										SetKey(Value="PreGripPose"),
										transitions={'done': 'say back'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:367 y:505
			OperatableStateMachine.add('open',
										SetGripperState(width=0.15, effort=0),
										transitions={'object': 'pre', 'no_object': 'pre'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:254 y:218
			OperatableStateMachine.add('get',
										GetSpeech(watchdog=10),
										transitions={'done': 'thanks', 'nothing': 'open', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:33 y:269
			OperatableStateMachine.add('thanks',
										RegexTester(regex=".*((thank)|(you)).*"),
										transitions={'true': 'say pleasure', 'false': 'open'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:102 y:399
			OperatableStateMachine.add('say pleasure',
										SaraSay(sentence="It's a pleasure to serve you", emotion=1, block=False),
										transitions={'done': 'open'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:42
			OperatableStateMachine.add('give',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'say here', 'failed': 'say here'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:266 y:132
			OperatableStateMachine.add('say here',
										SaraSayKey(Format=lambda x: "Here is the "+x+" you asked for.", emotion=1, block=True),
										transitions={'done': 'get'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:516 y:549
			OperatableStateMachine.add('pre',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'done'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:150 y:39
			OperatableStateMachine.add('say back',
										SaraSay(sentence="I'm back", emotion=1, block=False),
										transitions={'done': 'give'},
										autonomy={'done': Autonomy.Off})


		# x:43 y:574
		_sm_set_keys_1 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'], output_keys=['id', 'color', 'room', 'type', 'name', 'relative', 'unrelative'])

		with _sm_set_keys_1:
			# x:30 y:40
			OperatableStateMachine.add('set1',
										SetKey(Value=None),
										transitions={'done': 'set2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'id'})

			# x:31 y:110
			OperatableStateMachine.add('set2',
										SetKey(Value=None),
										transitions={'done': 'set3'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'type'})

			# x:31 y:180
			OperatableStateMachine.add('set3',
										SetKey(Value=None),
										transitions={'done': 'set4'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'color'})

			# x:26 y:246
			OperatableStateMachine.add('set4',
										SetKey(Value=None),
										transitions={'done': 'get name'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'room'})

			# x:16 y:329
			OperatableStateMachine.add('get name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'set rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:30 y:407
			OperatableStateMachine.add('set rel',
										SetKey(Value=True),
										transitions={'done': 'set unrel'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:27 y:486
			OperatableStateMachine.add('set unrel',
										SetKey(Value=False),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'unrelative'})


		# x:720 y:74, x:608 y:499, x:746 y:288
		_sm_get_room_2 = OperatableStateMachine(outcomes=['found', 'unknown', 'error'], input_keys=['Action', 'expected_pose'], output_keys=['room_pose'])

		with _sm_get_room_2:
			# x:30 y:40
			OperatableStateMachine.add('set1',
										SetKey(Value=None),
										transitions={'done': 'set2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'id'})

			# x:263 y:49
			OperatableStateMachine.add('set2',
										SetKey(Value=None),
										transitions={'done': 'get room name'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'type'})

			# x:230 y:363
			OperatableStateMachine.add('get room name',
										CalculationState(calculation=lambda x: x[2]),
										transitions={'done': 'get room'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:438 y:308
			OperatableStateMachine.add('get room',
										WonderlandGetRoom(),
										transitions={'found': 'found', 'unknown': 'say unknown', 'error': 'error'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'type': 'type', 'expected_pose': 'expected_pose', 'room_pose': 'room_pose', 'room_name': 'room_name', 'room_type': 'room_type'})

			# x:471 y:499
			OperatableStateMachine.add('say unknown',
										SaraSayKey(Format=lambda x: "I don't know where is the "+x, emotion=1, block=True),
										transitions={'done': 'unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		# x:816 y:646, x:854 y:48
		_sm_bring_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['expected_pose', 'Action', 'robot_pose'])

		with _sm_bring_3:
			# x:37 y:26
			OperatableStateMachine.add('Set keys',
										_sm_set_keys_1,
										transitions={'done': 'log pose'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'id': 'id', 'color': 'color', 'room': 'room', 'type': 'type', 'name': 'name', 'relative': 'relative', 'unrelative': 'unrelative'})

			# x:134 y:348
			OperatableStateMachine.add('Move_to_Object',
										self.use_behavior(Action_MoveSM, 'Bring/Move_to_Object'),
										transitions={'finished': 'Action_pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'object_pose', 'relative': 'unrelative'})

			# x:138 y:251
			OperatableStateMachine.add('get object',
										WonderlandGetObject(),
										transitions={'found': 'Move_to_Object', 'unknown': 'say unknown', 'error': 'failed'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'color': 'color', 'room': 'room', 'type': 'type', 'expected_pose': 'expected_pose', 'object_pose': 'object_pose', 'object_name': 'object_name', 'object_color': 'object_color', 'object_room': 'object_room', 'object_type': 'object_type'})

			# x:807 y:238
			OperatableStateMachine.add('Move_Back',
										self.use_behavior(Action_MoveSM, 'Bring/Move_Back'),
										transitions={'finished': 'Giving back', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robot_pose', 'relative': 'unrelative'})

			# x:54 y:659
			OperatableStateMachine.add('Move_Forward',
										self.use_behavior(Action_MoveSM, 'Bring/Move_Forward'),
										transitions={'finished': 'Action_pick', 'failed': 'Action_pick'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'decal_pose', 'relative': 'relative'})

			# x:237 y:511
			OperatableStateMachine.add('for',
										ForLoop(repeat=2),
										transitions={'do': 'say closer', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:252 y:643
			OperatableStateMachine.add('gen decal',
										GenPoseEuler(x=0.35, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Move_Forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'decal_pose'})

			# x:38 y:468
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Bring/Action_pick'),
										transitions={'success': 'Move_Back', 'too far': 'for', 'unreachable': 'finished', 'not seen': 'finished', 'critical fail': 'failed', 'missed': 'finished'},
										autonomy={'success': Autonomy.Inherit, 'too far': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not seen': Autonomy.Inherit, 'critical fail': Autonomy.Inherit, 'missed': Autonomy.Inherit},
										remapping={'object': 'name', 'grip_pose': 'grip_pose'})

			# x:247 y:581
			OperatableStateMachine.add('say closer',
										SaraSay(sentence="I need to get closer", emotion=1, block=True),
										transitions={'done': 'gen decal'},
										autonomy={'done': Autonomy.Off})

			# x:312 y:219
			OperatableStateMachine.add('say unknown',
										SaraSayKey(Format=lambda x: "I don't know any "+x, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:704 y:441
			OperatableStateMachine.add('Giving back',
										_sm_giving_back_0,
										transitions={'fail': 'failed', 'done': 'finished'},
										autonomy={'fail': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'name': 'name'})

			# x:133 y:161
			OperatableStateMachine.add('log pose',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'get object'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'expected_pose'})



		with _state_machine:
			# x:105 y:29
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'get robot pose', 'false': 'say no object given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:285 y:73
			OperatableStateMachine.add('say no object given',
										SaraSay(sentence="You didn't told me what to bring", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:70 y:240
			OperatableStateMachine.add('cond3',
										CheckConditionState(predicate=lambda x: x[3] != ''),
										transitions={'true': 'say3', 'false': 'set beneficiary to you'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:137 y:362
			OperatableStateMachine.add('say3',
										SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1]+" to "+x[3], emotion=1, block=True),
										transitions={'done': 'cond2'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:399 y:283
			OperatableStateMachine.add('say bring',
										SaraSayKey(Format=lambda x: "I'm now gonna bring the "+x[1], emotion=1, block=True),
										transitions={'done': 'cond2'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:251 y:208
			OperatableStateMachine.add('set beneficiary to you',
										SetKey(Value="you"),
										transitions={'done': 'say bring'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'beneficiary'})

			# x:665 y:399
			OperatableStateMachine.add('Bring',
										_sm_bring_3,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'expected_pose': 'expected_pose', 'Action': 'Action', 'robot_pose': 'robot_pose'})

			# x:303 y:379
			OperatableStateMachine.add('cond2',
										CheckConditionState(predicate=lambda x: x[2]!=''),
										transitions={'true': 'Get room', 'false': 'get expected pose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:26 y:125
			OperatableStateMachine.add('get robot pose',
										Get_Robot_Pose(),
										transitions={'done': 'cond3'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'robot_pose'})

			# x:472 y:595
			OperatableStateMachine.add('Get room',
										_sm_get_room_2,
										transitions={'found': 'Bring', 'unknown': 'get expected pose', 'error': 'failed'},
										autonomy={'found': Autonomy.Inherit, 'unknown': Autonomy.Inherit, 'error': Autonomy.Inherit},
										remapping={'Action': 'Action', 'expected_pose': 'robot_pose', 'room_pose': 'expected_pose'})

			# x:224 y:603
			OperatableStateMachine.add('get expected pose',
										CalculationState(calculation=lambda x: x),
										transitions={'done': 'Bring'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'robot_pose', 'output_value': 'expected_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
