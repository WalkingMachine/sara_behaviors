#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_return_to_origin')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_origin.wonderland_get_origin_sm import Wonderland_Get_OriginSM
from sara_flexbe_states.Wonderland_Get_Waypoint import Wonderland_Get_Waypoint
from sara_flexbe_states.sara_move_base import SaraMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jul 17 2017
@author: Nicolas Nadeau
'''
class Return_to_OriginSM(Behavior):
	'''
	Make SARA move back to an old origin
	'''


	def __init__(self):
		super(Return_to_OriginSM, self).__init__()
		self.name = 'Return_to_Origin'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Wonderland_Get_OriginSM, 'Wonderland_Get_Origin')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:795 y:302, x:299 y:325
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name', 'index'])
		_state_machine.userdata.name = "origin"
		_state_machine.userdata.index = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:73 y:86
			OperatableStateMachine.add('Wonderland_Get_Origin',
										self.use_behavior(Wonderland_Get_OriginSM, 'Wonderland_Get_Origin'),
										transitions={'finished': 'Waypoint', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'waypoint': 'json_text'})

			# x:522 y:88
			OperatableStateMachine.add('Waypoint',
										Wonderland_Get_Waypoint(index_function=lambda x: 0),
										transitions={'done': 'Move', 'no_waypoint': 'failed', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'no_waypoint': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'json_text', 'input_value': 'index', 'id': 'id', 'name': 'name', 'x': 'x', 'y': 'y', 'theta': 'theta', 'pose': 'pose'})

			# x:878 y:173
			OperatableStateMachine.add('Move',
										SaraMoveBase(),
										transitions={'arrived': 'finished', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
