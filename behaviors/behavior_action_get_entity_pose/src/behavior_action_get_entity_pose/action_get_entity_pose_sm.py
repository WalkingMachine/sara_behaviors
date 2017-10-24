#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_get_entity_pose')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_set_angle import SaraSetHeadAngle
from sara_flexbe_states.get_box_center import GetBoxCenter
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Action_get_entity_poseSM(Behavior):
	'''
	standard way to get the pose on an entity
	'''


	def __init__(self):
		super(Action_get_entity_poseSM, self).__init__()
		self.name = 'Action_get_entity_pose'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:786 y:167, x:479 y:566
		_state_machine = OperatableStateMachine(outcomes=['found', 'not found'], input_keys=['name'], output_keys=['pose'])
		_state_machine.userdata.name = "cup"
		_state_machine.userdata.pose = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


		with _state_machine:
			# x:53 y:106
			OperatableStateMachine.add('head1',
										SaraSetHeadAngle(angle=0.4),
										transitions={'done': 'w1'},
										autonomy={'done': Autonomy.Off})

			# x:60 y:232
			OperatableStateMachine.add('head2',
										SaraSetHeadAngle(angle=0.8),
										transitions={'done': 'w2'},
										autonomy={'done': Autonomy.Off})

			# x:458 y:306
			OperatableStateMachine.add('get box 2',
										GetBoxCenter(watchdog=3),
										transitions={'done': 'found', 'not_found': 'head3'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'box_name': 'name', 'point': 'pose'})

			# x:463 y:141
			OperatableStateMachine.add('get box',
										GetBoxCenter(watchdog=3),
										transitions={'done': 'found', 'not_found': 'head2'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'box_name': 'name', 'point': 'pose'})

			# x:56 y:389
			OperatableStateMachine.add('head3',
										SaraSetHeadAngle(angle=0.0),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:460 y:444
			OperatableStateMachine.add('get box 3',
										GetBoxCenter(watchdog=3),
										transitions={'done': 'found', 'not_found': 'not found'},
										autonomy={'done': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'box_name': 'name', 'point': 'pose'})

			# x:281 y:104
			OperatableStateMachine.add('w1',
										WaitState(wait_time=2),
										transitions={'done': 'get box'},
										autonomy={'done': Autonomy.Off})

			# x:293 y:268
			OperatableStateMachine.add('w2',
										WaitState(wait_time=2),
										transitions={'done': 'get box 2'},
										autonomy={'done': Autonomy.Off})

			# x:295 y:416
			OperatableStateMachine.add('w3',
										WaitState(wait_time=2),
										transitions={'done': 'get box 3'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
