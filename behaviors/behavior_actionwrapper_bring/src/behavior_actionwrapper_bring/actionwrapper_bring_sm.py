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
		_state_machine.userdata.Action = ["Bring","cup", "",""]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:43 y:574
		_sm_set_keys_0 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'], output_keys=['id', 'color', 'room', 'type', 'name', 'relative', 'unrelative'])

		with _sm_set_keys_0:
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
		_sm_get_room_1 = OperatableStateMachine(outcomes=['found', 'unknown', 'error'], input_keys=['Action', 'expected_pose'], output_keys=['expected_pose'])

		with _sm_get_room_1:
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

			# x:484 y:360
			OperatableStateMachine.add('get room',
										WonderlandGetRoom(),
										transitions={'found': 'found', 'unknown': 'say unknown', 'error': 'error'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'type': 'type', 'expected_pose': 'expected_pose', 'room_pose': 'expected_pose', 'room_name': 'room_name', 'room_type': 'room_type'})

			# x:471 y:499
			OperatableStateMachine.add('say unknown',
										SaraSayKey(Format=lambda x: "I don't know where is the "+x, emotion=1, block=True),
										transitions={'done': 'unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})


		# x:844 y:545, x:854 y:48
		_sm_bring_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['expected_pose', 'Action', 'robot_pose'])

		with _sm_bring_2:
			# x:37 y:26
			OperatableStateMachine.add('Set keys',
										_sm_set_keys_0,
										transitions={'done': 'get object'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'id': 'id', 'color': 'color', 'room': 'room', 'type': 'type', 'name': 'name', 'relative': 'relative', 'unrelative': 'unrelative'})

			# x:39 y:344
			OperatableStateMachine.add('Move_to_Object',
										self.use_behavior(Action_MoveSM, 'Bring/Move_to_Object'),
										transitions={'finished': 'Action_pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'expected_pose', 'relative': 'unrelative'})

			# x:85 y:208
			OperatableStateMachine.add('get object',
										WonderlandGetObject(),
										transitions={'found': 'Move_to_Object', 'unknown': 'say unknown', 'error': 'failed'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'color': 'color', 'room': 'room', 'type': 'type', 'expected_pose': 'expected_pose', 'object_pose': 'object_pose', 'object_name': 'object_name', 'object_color': 'object_color', 'object_room': 'object_room', 'object_type': 'object_type'})

			# x:807 y:238
			OperatableStateMachine.add('Move_Back',
										self.use_behavior(Action_MoveSM, 'Bring/Move_Back'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'robot_pose', 'relative': 'unrelative'})

			# x:20 y:651
			OperatableStateMachine.add('Move_Forward',
										self.use_behavior(Action_MoveSM, 'Bring/Move_Forward'),
										transitions={'finished': 'Action_pick', 'failed': 'Action_pick'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'decal_pose', 'relative': 'relative'})

			# x:185 y:472
			OperatableStateMachine.add('for',
										ForLoop(repeat=2),
										transitions={'do': 'say closer', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:173 y:601
			OperatableStateMachine.add('gen decal',
										GenPoseEuler(x=0.35, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Move_Forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'decal_pose'})

			# x:34 y:428
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Bring/Action_pick'),
										transitions={'success': 'Move_Back', 'too far': 'for', 'unreachable': 'finished', 'not seen': 'finished', 'critical fail': 'failed', 'missed': 'finished'},
										autonomy={'success': Autonomy.Inherit, 'too far': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not seen': Autonomy.Inherit, 'critical fail': Autonomy.Inherit, 'missed': Autonomy.Inherit},
										remapping={'object': 'name', 'grip_pose': 'grip_pose'})

			# x:178 y:537
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
										_sm_bring_2,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'expected_pose': 'robot_pose', 'Action': 'Action', 'robot_pose': 'robot_pose'})

			# x:374 y:452
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

			# x:479 y:605
			OperatableStateMachine.add('Get room',
										_sm_get_room_1,
										transitions={'found': 'Bring', 'unknown': 'get expected pose', 'error': 'failed'},
										autonomy={'found': Autonomy.Inherit, 'unknown': Autonomy.Inherit, 'error': Autonomy.Inherit},
										remapping={'Action': 'Action', 'expected_pose': 'robot_pose'})

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
