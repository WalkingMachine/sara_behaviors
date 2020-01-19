#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.sara_move_base import SaraMoveBase
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
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:194 y:348, x:15 y:144
		_state_machine = OperatableStateMachine(outcomes=['Done', 'Fail'], input_keys=['DoorName'])
		_state_machine.userdata.DoorName = "door"
		_state_machine.userdata.otherSide = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:324
		_sm_manage_door_opening_0 = OperatableStateMachine(outcomes=['done'], output_keys=['otherSide'])

		with _sm_manage_door_opening_0:
			# x:41 y:40
			OperatableStateMachine.add('Wait for door 1',
										DoorDetector(timeout=1),
										transitions={'done': 'genfront', 'failed': 'door closed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:199 y:43
			OperatableStateMachine.add('door closed',
										SaraSay(sentence="This door is closed. I need an human.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'wait for door 2'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:151
			OperatableStateMachine.add('genfront',
										GenPoseEuler(x=1.5, y=0, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'otherSide'})

			# x:357 y:44
			OperatableStateMachine.add('wait for door 2',
										DoorDetector(timeout=5),
										transitions={'done': 'Thanks', 'failed': 'callhelp'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:534 y:45
			OperatableStateMachine.add('callhelp',
										SaraSay(sentence="Can someone open this door for me. Please.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'wait for door 2'},
										autonomy={'done': Autonomy.Off})

			# x:348 y:156
			OperatableStateMachine.add('Thanks',
										SaraSay(sentence="Thank you!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'genfront'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:155 y:30
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'Manage door opening', 'failed': 'Fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'DoorName'})

			# x:154 y:132
			OperatableStateMachine.add('Manage door opening',
										_sm_manage_door_opening_0,
										transitions={'done': 'move to the other side'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'otherSide': 'otherSide'})

			# x:160 y:234
			OperatableStateMachine.add('move to the other side',
										SaraMoveBase(reference="base_link"),
										transitions={'arrived': 'Done', 'failed': 'Fail'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'otherSide'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
