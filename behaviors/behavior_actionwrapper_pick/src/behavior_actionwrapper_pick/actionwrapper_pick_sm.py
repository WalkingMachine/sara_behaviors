#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.Wonderland_Get_Object import WonderlandGetObject
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_pick.action_pick_sm import Action_pickSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_PickSM(Behavior):
	'''
	action wrapper pour pick
	'''


	def __init__(self):
		super(ActionWrapper_PickSM, self).__init__()
		self.name = 'ActionWrapper_Pick'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'pick/Action_Move')
		self.add_behavior(Action_MoveSM, 'pick/Forward/Action_Move_2')
		self.add_behavior(Action_pickSM, 'pick/Action_pick')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 506 16 
		# Pick|n1- object|n2- where to find it



	def create(self):
		# x:727 y:189, x:725 y:372
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Action', 'ObjectInGripper'])
		_state_machine.userdata.Action = ["Pick","cup",""]
		_state_machine.userdata.ObjectInGripper = False
		_state_machine.userdata.room = 1
		_state_machine.userdata.id = None
		_state_machine.userdata.color = None
		_state_machine.userdata.type = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:516 y:297, x:455 y:109
		_sm_forward_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_forward_0:
			# x:47 y:28
			OperatableStateMachine.add('gen pose',
										GenPoseEuler(x=0.35, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'set rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:56 y:143
			OperatableStateMachine.add('set rel',
										SetKey(Value=True),
										transitions={'done': 'Action_Move_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:43 y:253
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(Action_MoveSM, 'pick/Forward/Action_Move_2'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})


		# x:437 y:171
		_sm_set_keys_1 = OperatableStateMachine(outcomes=['done'], output_keys=['id', 'color', 'room', 'type', 'expected_pose', 'relative'])

		with _sm_set_keys_1:
			# x:34 y:40
			OperatableStateMachine.add('set id',
										SetKey(Value=None),
										transitions={'done': 'set color'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'id'})

			# x:34 y:191
			OperatableStateMachine.add('set type',
										SetKey(Value=None),
										transitions={'done': 'set room'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'type'})

			# x:35 y:269
			OperatableStateMachine.add('set room',
										SetKey(Value=None),
										transitions={'done': 'get pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'room'})

			# x:30 y:112
			OperatableStateMachine.add('set color',
										SetKey(Value=None),
										transitions={'done': 'set type'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'color'})

			# x:268 y:282
			OperatableStateMachine.add('set rel',
										SetKey(Value=False),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:108 y:361
			OperatableStateMachine.add('get pose',
										Get_Robot_Pose(),
										transitions={'done': 'set rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'expected_pose'})


		# x:30 y:325
		_sm_get_informations_2 = OperatableStateMachine(outcomes=['done'], input_keys=['Action'], output_keys=['name'])

		with _sm_get_informations_2:
			# x:62 y:117
			OperatableStateMachine.add('get name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'get location'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:60 y:203
			OperatableStateMachine.add('get location',
										CalculationState(calculation=lambda x: x[2]),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'location'})


		# x:778 y:25, x:580 y:518
		_sm_pick_3 = OperatableStateMachine(outcomes=['success', 'failed'], input_keys=['Action'])

		with _sm_pick_3:
			# x:42 y:31
			OperatableStateMachine.add('Get informations',
										_sm_get_informations_2,
										transitions={'done': 'Set keys'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'name': 'name'})

			# x:738 y:120
			OperatableStateMachine.add('say fail',
										SaraSayKey(Format=lambda x: "Sorry, I failed to get the "+x, emotion=1, block=True),
										transitions={'done': 'success'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:35 y:381
			OperatableStateMachine.add('Get object',
										WonderlandGetObject(),
										transitions={'found': 'Action_Move', 'unknown': 'say unknow', 'error': 'memory'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'color': 'color', 'room': 'room', 'type': 'type', 'expected_pose': 'expected_pose', 'object_pose': 'object_pose', 'object_name': 'object_name', 'object_color': 'object_color', 'object_room': 'object_room', 'object_type': 'object_type'})

			# x:14 y:216
			OperatableStateMachine.add('Set keys',
										_sm_set_keys_1,
										transitions={'done': 'Get object'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'id': 'id', 'color': 'color', 'room': 'room', 'type': 'type', 'expected_pose': 'expected_pose', 'relative': 'relative'})

			# x:45 y:585
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'pick/Action_Move'),
										transitions={'finished': 'Action_pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'object_pose', 'relative': 'relative'})

			# x:200 y:311
			OperatableStateMachine.add('Forward',
										_sm_forward_0,
										transitions={'finished': 'Action_pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:268 y:123
			OperatableStateMachine.add('for',
										ForLoop(repeat=2),
										transitions={'do': 'get closer', 'end': 'say fail'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:417 y:112
			OperatableStateMachine.add('say unreachable',
										SaraSay(sentence="I can't reach it", emotion=1, block=True),
										transitions={'done': 'say fail'},
										autonomy={'done': Autonomy.Off})

			# x:260 y:235
			OperatableStateMachine.add('get closer',
										SaraSay(sentence="I need to get closer", emotion=1, block=True),
										transitions={'done': 'Forward'},
										autonomy={'done': Autonomy.Off})

			# x:229 y:426
			OperatableStateMachine.add('say unknow',
										SaraSayKey(Format=lambda x: "I don't know any "+x, emotion=1, block=True),
										transitions={'done': 'say fail'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:211 y:505
			OperatableStateMachine.add('memory',
										SaraSay(sentence="Strange, I lost contact with my memory", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:202 y:39
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'pick/Action_pick'),
										transitions={'success': 'success', 'too far': 'for', 'unreachable': 'say unreachable', 'not seen': 'say fail', 'critical fail': 'failed', 'missed': 'say fail'},
										autonomy={'success': Autonomy.Inherit, 'too far': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not seen': Autonomy.Inherit, 'critical fail': Autonomy.Inherit, 'missed': Autonomy.Inherit},
										remapping={'object': 'name', 'grip_pose': 'grip_pose'})



		with _state_machine:
			# x:36 y:47
			OperatableStateMachine.add('check object in gripper',
										CheckConditionState(predicate=lambda x: x),
										transitions={'true': 'finished', 'false': 'cond'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'ObjectInGripper'})

			# x:223 y:185
			OperatableStateMachine.add('object given',
										SaraSayKey(Format=lambda x: "I'm going to pick that "+x[1], emotion=1, block=True),
										transitions={'done': 'pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:41 y:189
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] == ''),
										transitions={'true': 'not told', 'false': 'object given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:409 y:181
			OperatableStateMachine.add('pick',
										_sm_pick_3,
										transitions={'success': 'finished', 'failed': 'failed'},
										autonomy={'success': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:49 y:378
			OperatableStateMachine.add('not told',
										SaraSay(sentence="You didn't told me what to pick", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
