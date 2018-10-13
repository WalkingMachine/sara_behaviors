#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_restaurant2018')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_action_move.action_move_sm import Action_MoveSM
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_action_pick.action_pick_sm import Action_pickSM
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_give.action_give_sm import Action_GiveSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 12 2018
@author: Raphael Duchaine
'''
class restaurant2018SM(Behavior):
	'''
	Mockup pour la video de qualification 2019
	'''


	def __init__(self):
		super(restaurant2018SM, self).__init__()
		self.name = 'restaurant2018'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Move_to_Start')
		self.add_behavior(Action_MoveSM, 'Move to client')
		self.add_behavior(Action_MoveSM, 'Action_Move')
		self.add_behavior(Action_pickSM, 'Action_pick')
		self.add_behavior(Action_MoveSM, 'Return to client')
		self.add_behavior(Action_GiveSM, 'GiveToClient')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 424 314 
		# get object on table

		# O 626 404 
		# Give to Client



	def create(self):
		# x:804 y:313, x:333 y:477
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.pose = null
		_state_machine.userdata.relative = false
		_state_machine.userdata.start = null
		_state_machine.userdata.objectID = 0
		_state_machine.userdata.name = "bottle"
		_state_machine.userdata.temporaryVariablesToChange = "Change Everything above"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:58 y:22
			OperatableStateMachine.add('Move_to_Start',
										self.use_behavior(Action_MoveSM, 'Move_to_Start'),
										transitions={'finished': 'waitForClientWaving', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'start', 'relative': 'relative'})

			# x:246 y:27
			OperatableStateMachine.add('waitForClientWaving',
										WaitState(wait_time=5),
										transitions={'done': 'Move to client'},
										autonomy={'done': Autonomy.Off})

			# x:414 y:23
			OperatableStateMachine.add('Move to client',
										self.use_behavior(Action_MoveSM, 'Move to client'),
										transitions={'finished': 'TakeOrder', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:625 y:55
			OperatableStateMachine.add('TakeOrder',
										SaraSay(sentence="Hi! How may I serve you?", emotion=1, block=True),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:30 y:118
			OperatableStateMachine.add('GetOrder',
										GetSpeech(watchdog=10),
										transitions={'done': 'RepeatOrder', 'nothing': 'failed', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'order'})

			# x:481 y:115
			OperatableStateMachine.add('TellOrder',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'WaitForItems'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:261 y:121
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'TellOrder', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:596 y:135
			OperatableStateMachine.add('WaitForItems',
										WaitState(wait_time=10),
										transitions={'done': 'listVisibleEntities'},
										autonomy={'done': Autonomy.Off})

			# x:429 y:255
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'Return to client', 'unreachable': 'failed', 'not found': 'failed', 'dropped': 'failed'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'objectID'})

			# x:45 y:246
			OperatableStateMachine.add('listVisibleEntities',
										list_entities_by_name(frontality_level=0.5, distance_max=5),
										transitions={'found': 'Action_pick', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'name', 'entity_list': 'entity_list', 'number': 'number'})

			# x:571 y:230
			OperatableStateMachine.add('Return to client',
										self.use_behavior(Action_MoveSM, 'Return to client'),
										transitions={'finished': 'GiveToClient', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:104 y:173
			OperatableStateMachine.add('RepeatOrder',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:622 y:341
			OperatableStateMachine.add('GiveToClient',
										self.use_behavior(Action_GiveSM, 'GiveToClient'),
										transitions={'Given': 'finished', 'Person_not_found': 'failed', 'No_object_in_hand': 'failed', 'fail': 'failed'},
										autonomy={'Given': Autonomy.Inherit, 'Person_not_found': Autonomy.Inherit, 'No_object_in_hand': Autonomy.Inherit, 'fail': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
