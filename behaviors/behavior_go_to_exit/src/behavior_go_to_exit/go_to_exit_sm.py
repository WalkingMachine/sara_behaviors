#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_go_to_exit')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from behavior_wonderland_get_doors.wonderland_get_doors_sm import Wonderland_Get_DoorsSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jul 28 2017
@author: Redouane Laref
'''
class Go_to_exitSM(Behavior):
	'''
	go to exit
	'''


	def __init__(self):
		super(Go_to_exitSM, self).__init__()
		self.name = 'Go_to_exit'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_DoorsSM, 'Wonderland_Get_Doors')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:533 y:359, x:680 y:371
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:163 y:78
			OperatableStateMachine.add('say exiting',
										SaraSay(sentence="I'am going to exit the arena now", emotion=1),
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Off})

			# x:301 y:90
			OperatableStateMachine.add('wait',
										WaitState(wait_time=3),
										transitions={'done': 'Wonderland_Get_Doors'},
										autonomy={'done': Autonomy.Off})

			# x:725 y:127
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'exit_pose'})

			# x:193 y:165
			OperatableStateMachine.add('Wonderland_Get_Doors',
										self.use_behavior(Wonderland_Get_DoorsSM, 'Wonderland_Get_Doors'),
										transitions={'done': 'move', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'exit_pose': 'exit_pose', 'entrance_id': 'entrance_id', 'entrance_pose': 'entrance_pose', 'entrance_rooms_id': 'entrance_rooms_id', 'entrance_rooms_names': 'entrance_rooms_names', 'exit_id': 'exit_id', 'exit_rooms_id': 'exit_rooms_id', 'exit_rooms_names': 'exit_rooms_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
