#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_restaurant2018')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from flexbe_states.log_key_state import LogKeyState
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
from behavior_actionwrapper_give.actionwrapper_give_sm import ActionWrapper_GiveSM
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
		self.add_behavior(ActionWrapper_MoveSM, 'ReturnToClient')
		self.add_behavior(ActionWrapper_MoveSM, 'MoveToClient')
		self.add_behavior(ActionWrapper_MoveSM, 'MoveToStart')
		self.add_behavior(ActionWrapper_MoveSM, 'MoveToBarman')
		self.add_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick')
		self.add_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 496 664 
		# get object on table

		# O 112 640 
		# Give to Client



	def create(self):
		# x:30 y:589, x:474 y:278
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = ""
		_state_machine.userdata.order = "bottle"
		_state_machine.userdata.Action2 = ["Give", "client"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:32 y:383
			OperatableStateMachine.add('setActionClient',
										SetKey(Value=["move","dining table"]),
										transitions={'done': 'setActionStart'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionClient'})

			# x:625 y:28
			OperatableStateMachine.add('TakeOrder',
										SaraSay(sentence="Hi! How may I serve you?", emotion=1, block=True),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:709 y:70
			OperatableStateMachine.add('GetOrder',
										GetSpeech(watchdog=10),
										transitions={'done': 'RepeatOrder', 'nothing': 'failed', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'order'})

			# x:798 y:284
			OperatableStateMachine.add('TellOrder',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'WaitForItems'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:782 y:363
			OperatableStateMachine.add('WaitForItems',
										WaitState(wait_time=10),
										transitions={'done': 'listVisibleEntities'},
										autonomy={'done': Autonomy.Off})

			# x:793 y:482
			OperatableStateMachine.add('listVisibleEntities',
										list_entities_by_name(frontality_level=0.5, distance_max=10),
										transitions={'found': 'logkey', 'not_found': 'listVisibleEntities'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'order', 'entity_list': 'entity_list', 'number': 'number'})

			# x:828 y:92
			OperatableStateMachine.add('RepeatOrder',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'MoveToBarman'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:685 y:529
			OperatableStateMachine.add('closerElement',
										CalculationState(calculation=lambda x: ["pick", x[0].name]),
										transitions={'done': 'ActionWrapper_Pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity_list', 'output_value': 'Action'})

			# x:301 y:581
			OperatableStateMachine.add('ReturnToClient',
										self.use_behavior(ActionWrapper_MoveSM, 'ReturnToClient'),
										transitions={'finished': 'ActionWrapper_Give', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionClient'})

			# x:415 y:14
			OperatableStateMachine.add('MoveToClient',
										self.use_behavior(ActionWrapper_MoveSM, 'MoveToClient'),
										transitions={'finished': 'TakeOrder', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionClient'})

			# x:34 y:36
			OperatableStateMachine.add('MoveToStart',
										self.use_behavior(ActionWrapper_MoveSM, 'MoveToStart'),
										transitions={'finished': 'waitForClientWaving', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionStart'})

			# x:773 y:204
			OperatableStateMachine.add('MoveToBarman',
										self.use_behavior(ActionWrapper_MoveSM, 'MoveToBarman'),
										transitions={'finished': 'TellOrder', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionBarman'})

			# x:53 y:287
			OperatableStateMachine.add('setActionStart',
										SetKey(Value=["move","Operator"]),
										transitions={'done': 'setActionBarman'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionStart'})

			# x:56 y:144
			OperatableStateMachine.add('setActionBarman',
										SetKey(Value=["move","bar"]),
										transitions={'done': 'ReturnToClient'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionBarman'})

			# x:246 y:27
			OperatableStateMachine.add('waitForClientWaving',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToClient'},
										autonomy={'done': Autonomy.Off})

			# x:828 y:595
			OperatableStateMachine.add('logkey',
										LogKeyState(text="List:{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'closerElement'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity_list'})

			# x:498 y:597
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick'),
										transitions={'finished': 'ReturnToClient', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:103 y:579
			OperatableStateMachine.add('ActionWrapper_Give',
										self.use_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action2'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
