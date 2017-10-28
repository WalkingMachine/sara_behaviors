#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.Wonderland_Get_Room import WonderlandGetRoom
from flexbe_states.log_key_state import LogKeyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe la Madeleine
'''
class Test_continueSM(Behavior):
	'''
	test the continue button
	'''


	def __init__(self):
		super(Test_continueSM, self).__init__()
		self.name = 'Test_continue'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Group/Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

	# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:649 y:285, x:641 y:194
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.id = None
		_state_machine.userdata.name = "living room"
		_state_machine.userdata.type = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:757 y:475, x:762 y:135
		_sm_group_0 = OperatableStateMachine(outcomes=['failed', 'finished'], input_keys=['id', 'name', 'type'])

		with _sm_group_0:
			# x:33 y:32
			OperatableStateMachine.add('get pose',
										Get_Robot_Pose(),
										transitions={'done': 'Get room'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'expected_pose'})

			# x:401 y:460
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Group/Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'room_pose', 'relative': 'relative'})

			# x:164 y:540
			OperatableStateMachine.add('set',
										SetKey(Value=False),
										transitions={'done': 'log'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:184 y:304
			OperatableStateMachine.add('Get room',
										WonderlandGetRoom(),
										transitions={'found': 'set', 'unknown': 'failed', 'error': 'failed'},
										autonomy={'found': Autonomy.Off, 'unknown': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'id': 'id', 'name': 'name', 'type': 'type', 'expected_pose': 'expected_pose', 'room_pose': 'room_pose', 'room_name': 'room_name', 'room_type': 'room_type'})

			# x:278 y:566
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'room_pose'})



		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('starting test',
										SaraSay(sentence="Starting test", emotion=1, block=True),
										transitions={'done': 'Group'},
										autonomy={'done': Autonomy.Off})

			# x:462 y:357
			OperatableStateMachine.add('test succeed',
										SaraSay(sentence="Test succeed", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:231 y:181
			OperatableStateMachine.add('Group',
										_sm_group_0,
										transitions={'failed': 'test failed', 'finished': 'test succeed'},
										autonomy={'failed': Autonomy.Inherit, 'finished': Autonomy.Inherit},
										remapping={'id': 'id', 'name': 'name', 'type': 'type'})

			# x:462 y:122
			OperatableStateMachine.add('test failed',
										SaraSay(sentence="Test failed", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
