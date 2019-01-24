#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 14 2018
@author: Philippe La Madeleine
'''
class Action_Pass_DoorSM(Behavior):
	'''
	Make sara get through a door
	'''


	def __init__(self):
		super(Action_Pass_DoorSM, self).__init__()
		self.name = 'Action_Pass_Door'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move_2')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:149 y:709, x:27 y:350
		_state_machine = OperatableStateMachine(outcomes=['Done', 'Fail'], input_keys=['DoorPose1'])
		_state_machine.userdata.DoorPose1 = 0
		_state_machine.userdata.DoorPose2 = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:184 y:32
			OperatableStateMachine.add('not rel',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:160 y:212
			OperatableStateMachine.add('Wait for door 1',
										DoorDetector(timeout=1),
										transitions={'done': 'genfront', 'failed': 'door closed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:314 y:210
			OperatableStateMachine.add('door closed',
										SaraSay(sentence="This door is closed. I need an human.", emotion=1, block=True),
										transitions={'done': 'wait for door 2'},
										autonomy={'done': Autonomy.Off})

			# x:120 y:572
			OperatableStateMachine.add('Action_Move_2',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move_2'),
										transitions={'finished': 'Done', 'failed': 'Fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:151 y:355
			OperatableStateMachine.add('genfront',
										GenPoseEuler(x=1.5, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'set rel'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:155 y:468
			OperatableStateMachine.add('set rel',
										SetKey(Value=True),
										transitions={'done': 'Action_Move_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:469 y:199
			OperatableStateMachine.add('wait for door 2',
										DoorDetector(timeout=5),
										transitions={'done': 'Thanks', 'failed': 'callhelp'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:649 y:200
			OperatableStateMachine.add('callhelp',
										SaraSay(sentence="Can someone open this door for me. Please.", emotion=1, block=True),
										transitions={'done': 'wait for door 2'},
										autonomy={'done': Autonomy.Off})

			# x:474 y:337
			OperatableStateMachine.add('Thanks',
										SaraSay(sentence="Thank you!", emotion=1, block=True),
										transitions={'done': 'genfront'},
										autonomy={'done': Autonomy.Off})

			# x:160 y:115
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'Wait for door 1', 'failed': 'Fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'DoorPose1', 'relative': 'relative'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
