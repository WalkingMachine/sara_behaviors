#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_test_continue')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.SetKey import SetKey
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
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

	# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:649 y:285, x:641 y:194
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.sentence = "bring the cup from the table to the room"
		_state_machine.userdata.HighFIFO = []
		_state_machine.userdata.MedFIFO = []
		_state_machine.userdata.LowFIFO = []
		_state_machine.userdata.DoNow = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:87 y:70
			OperatableStateMachine.add('gen',
										GenPoseEuler(x=-1, y=-2, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'set'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:261 y:186
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:98 y:180
			OperatableStateMachine.add('set',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
