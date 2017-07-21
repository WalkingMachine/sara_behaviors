#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_wonderland_list_rooms')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Wonderland_Request import Wonderland_Request
from sara_flexbe_states.Wonderland_List_Something import Wonderland_List_Something
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Jul 16 2017
@author: Lucas Maurice
'''
class Wonderland_List_RoomsSM(Behavior):
	'''
	List all rooms.
	'''


	def __init__(self):
		super(Wonderland_List_RoomsSM, self).__init__()
		self.name = 'Wonderland_List_Rooms'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:773 y:86, x:417 y:226, x:609 y:222
		_state_machine = OperatableStateMachine(outcomes=['done', 'failed', 'empty'], output_keys=['ids', 'names'])
		_state_machine.userdata.ids = [""]
		_state_machine.userdata.names = [""]
		_state_machine.userdata.url = "rooms"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:231 y:81
			OperatableStateMachine.add('Wonderland_Request',
										Wonderland_Request(),
										transitions={'done': 'Wonderland_List_Something', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'url': 'url', 'response': 'entity'})

			# x:499 y:81
			OperatableStateMachine.add('Wonderland_List_Something',
										Wonderland_List_Something(),
										transitions={'done': 'done', 'empty': 'empty', 'error': 'failed'},
										autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off, 'error': Autonomy.Off},
										remapping={'json_text': 'entity', 'ids': 'ids', 'names': 'names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
