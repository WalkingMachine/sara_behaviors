#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_test2')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Wonderland_Get_Entity_Room import Wonderland_Get_Entity_Room
from sara_flexbe_states.test_log import test_log
from sara_flexbe_states.Wonderland_Get_Waypoint import Wonderland_Get_Waypoint
from behavior_wonderland_get_waypoint.wonderland_get_waypoint_sm import Wonderland_Get_WaypointSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Nicolas Nadeau
'''
class Wonderland_Test2SM(Behavior):
	'''
	Test state for wonderland2
	'''


	def __init__(self):
		super(Wonderland_Test2SM, self).__init__()
		self.name = 'Wonderland_Test2'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_WaypointSM, 'Wonderland_Get_Waypoint')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:834 y:68, x:299 y:325
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name', 'index'])
		_state_machine.userdata.name = "origin"
		_state_machine.userdata.index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:81 y:94
			OperatableStateMachine.add('Wonderland_Get_Waypoint',
										self.use_behavior(Wonderland_Get_WaypointSM, 'Wonderland_Get_Waypoint'),
										transitions={'finished': 'Waypoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint': 'json_text'})

			# x:650 y:63
			OperatableStateMachine.add('test_log',
										test_log(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'text': 'name'})

			# x:415 y:53
			OperatableStateMachine.add('Waypoint',
										Wonderland_Get_Waypoint(index_function=lambda x: 0),
										transitions={'done': 'test_log', 'no_waypoint': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_waypoint': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'index', 'id': 'id', 'name': 'name', 'x': 'x', 'y': 'y', 'theta': 'theta'})

			# x:517 y:404
			OperatableStateMachine.add('Wonderland_Get_Entity_Room',
										Wonderland_Get_Entity_Room(index_function=lambda x: x),
										transitions={'done': 'test_log', 'no_room': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_room': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'index', 'id': 'id', 'name': 'name', 'x1': 'x1', 'x2': 'x2', 'x3': 'x3', 'x4': 'x4', 'y1': 'y1', 'y2': 'y2', 'y3': 'y3', 'y4': 'y4'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
