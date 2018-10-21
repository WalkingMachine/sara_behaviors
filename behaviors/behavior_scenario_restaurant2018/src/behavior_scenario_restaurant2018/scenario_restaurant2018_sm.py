#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_restaurant2018')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from behavior_actionwrapper_give.actionwrapper_give_sm import ActionWrapper_GiveSM
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.calculation_state import CalculationState
from behavior_action_find.action_find_sm import Action_findSM
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 12 2018
@author: Raphael Duchaine
'''
class scenario_restaurant2018SM(Behavior):
	'''
	Mockup pour la video de qualification 2019
	'''


	def __init__(self):
		super(scenario_restaurant2018SM, self).__init__()
		self.name = 'scenario_restaurant2018'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(ActionWrapper_MoveSM, 'MoveToDiningRoom')
		self.add_behavior(ActionWrapper_MoveSM, 'MoveToBarman')
		self.add_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give')
		self.add_behavior(ActionWrapper_MoveSM, 'Spot and move to client/MoveToClient')
		self.add_behavior(Action_findSM, 'Wait for And Find Item/Action_find')
		self.add_behavior(ActionWrapper_PickSM, 'Pick Item/ActionWrapper_Pick')
		self.add_behavior(ActionWrapper_MoveSM, 'ReturnToClient')
		self.add_behavior(ActionWrapper_MoveSM, 'Return to Bar')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 517 664 
		# get object on table

		# O 112 630 
		# Give to Client

		# O 817 86 
		# Penser a reconnecter les Move 

		# ! 169 52 /Spot and move to client
		# TODO : Replace with a find person or something better

		# O 602 115 /Take Order
		# TODO: Confirm the order 



	def create(self):
		# x:149 y:458, x:474 y:278
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = ""
		_state_machine.userdata.order = "Bring me a bottle"
		_state_machine.userdata.Action2 = ["Give", ""]
		_state_machine.userdata.goodOrder = "no"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_pick_item_0 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['entity'])

		with _sm_pick_item_0:
			# x:397 y:40
			OperatableStateMachine.add('logkey',
										LogKeyState(text="Entity:{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'SetActionPick'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'entity'})

			# x:30 y:51
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'Pick Item/ActionWrapper_Pick'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'ActionPick'})

			# x:241 y:42
			OperatableStateMachine.add('SetActionPick',
										CalculationState(calculation=lambda x: ["pick", x.name]),
										transitions={'done': 'ActionWrapper_Pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'ActionPick'})


		# x:30 y:458, x:130 y:458
		_sm_wait_for_and_find_item_1 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['order'], output_keys=['entity'])

		with _sm_wait_for_and_find_item_1:
			# x:44 y:40
			OperatableStateMachine.add('TellOrder',
										SaraSayKey(Format=lambda x: "My client want a "+x.split()[-1], emotion=1, block=True),
										transitions={'done': 'WaitForItems'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:30 y:115
			OperatableStateMachine.add('WaitForItems',
										WaitState(wait_time=3),
										transitions={'done': 'Get last word of Order'},
										autonomy={'done': Autonomy.Off})

			# x:202 y:133
			OperatableStateMachine.add('Get last word of Order',
										CalculationState(calculation=lambda x:x.split()[-1]),
										transitions={'done': 'logObject'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'order', 'output_value': 'object'})

			# x:86 y:226
			OperatableStateMachine.add('Action_find',
										self.use_behavior(Action_findSM, 'Wait for And Find Item/Action_find'),
										transitions={'done': 'done', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'object', 'entity': 'entity'})

			# x:279 y:205
			OperatableStateMachine.add('logObject',
										LogKeyState(text="object:{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Action_find'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'object'})


		# x:30 y:458, x:100 y:461, x:1109 y:81
		_sm_take_order_2 = OperatableStateMachine(outcomes=['nothing', 'fail', 'done'], output_keys=['order'])

		with _sm_take_order_2:
			# x:30 y:40
			OperatableStateMachine.add('TakeOrder',
										SaraSay(sentence="Hi! How may I serve you?", emotion=1, block=True),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:154 y:70
			OperatableStateMachine.add('GetOrder',
										GetSpeech(watchdog=10),
										transitions={'done': 'RepeatOrder', 'nothing': 'nothing', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'order'})

			# x:272 y:45
			OperatableStateMachine.add('RepeatOrder',
										SaraSayKey(Format=lambda x: "Do you want a "+x.split()[-1], emotion=1, block=True),
										transitions={'done': 'YesOrNo'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'order'})

			# x:742 y:59
			OperatableStateMachine.add('CheckIfYes',
										CheckConditionState(predicate=lambda x: "yes" in x),
										transitions={'true': 'done', 'false': 'MayYouRepeat'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'goodOrder'})

			# x:452 y:29
			OperatableStateMachine.add('YesOrNo',
										GetSpeech(watchdog=5),
										transitions={'done': 'LogGoodOrder', 'nothing': 'MayYouRepeat', 'fail': 'MayYouRepeat'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'goodOrder'})

			# x:363 y:189
			OperatableStateMachine.add('MayYouRepeat',
										SaraSay(sentence="May you repeat your order, please?", emotion=1, block=True),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off})

			# x:587 y:14
			OperatableStateMachine.add('LogGoodOrder',
										LogKeyState(text="goodOrder:{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'CheckIfYes'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'goodOrder'})


		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_spot_and_move_to_client_3 = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['actionClient'])

		with _sm_spot_and_move_to_client_3:
			# x:30 y:50
			OperatableStateMachine.add('waitForClientWaving',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToClient'},
										autonomy={'done': Autonomy.Off})

			# x:36 y:243
			OperatableStateMachine.add('MoveToClient',
										self.use_behavior(ActionWrapper_MoveSM, 'Spot and move to client/MoveToClient'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionClient'})


		# x:30 y:458
		_sm_initialisation_4 = OperatableStateMachine(outcomes=['done'], output_keys=['actionClient', 'actionDiningRoom', 'actionBarman'])

		with _sm_initialisation_4:
			# x:81 y:80
			OperatableStateMachine.add('setActionClient',
										SetKey(Value=["move","dining table"]),
										transitions={'done': 'setActionDiningRoom'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionClient'})

			# x:51 y:183
			OperatableStateMachine.add('setActionDiningRoom',
										SetKey(Value=["move","Dining Room"]),
										transitions={'done': 'setActionBarman'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionDiningRoom'})

			# x:67 y:308
			OperatableStateMachine.add('setActionBarman',
										SetKey(Value=["move","bar"]),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'actionBarman'})



		with _state_machine:
			# x:54 y:264
			OperatableStateMachine.add('Initialisation',
										_sm_initialisation_4,
										transitions={'done': 'Take Order'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'actionClient': 'actionClient', 'actionDiningRoom': 'actionDiningRoom', 'actionBarman': 'actionBarman'})

			# x:43 y:102
			OperatableStateMachine.add('MoveToDiningRoom',
										self.use_behavior(ActionWrapper_MoveSM, 'MoveToDiningRoom'),
										transitions={'finished': 'Spot and move to client', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionDiningRoom'})

			# x:773 y:204
			OperatableStateMachine.add('MoveToBarman',
										self.use_behavior(ActionWrapper_MoveSM, 'MoveToBarman'),
										transitions={'finished': 'Wait for And Find Item', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionBarman'})

			# x:272 y:545
			OperatableStateMachine.add('ActionWrapper_Give',
										self.use_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give'),
										transitions={'finished': 'Return to Bar', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action2'})

			# x:335 y:32
			OperatableStateMachine.add('Spot and move to client',
										_sm_spot_and_move_to_client_3,
										transitions={'finished': 'Take Order', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'actionClient': 'actionClient'})

			# x:658 y:18
			OperatableStateMachine.add('Take Order',
										_sm_take_order_2,
										transitions={'nothing': 'failed', 'fail': 'failed', 'done': 'MoveToBarman'},
										autonomy={'nothing': Autonomy.Inherit, 'fail': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'order': 'order'})

			# x:803 y:320
			OperatableStateMachine.add('Wait for And Find Item',
										_sm_wait_for_and_find_item_1,
										transitions={'done': 'Pick Item', 'failed': 'failed'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'order': 'order', 'entity': 'entity'})

			# x:764 y:525
			OperatableStateMachine.add('Pick Item',
										_sm_pick_item_0,
										transitions={'finished': 'ReturnToClient', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'entity': 'entity'})

			# x:492 y:566
			OperatableStateMachine.add('ReturnToClient',
										self.use_behavior(ActionWrapper_MoveSM, 'ReturnToClient'),
										transitions={'finished': 'ActionWrapper_Give', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionClient'})

			# x:70 y:524
			OperatableStateMachine.add('Return to Bar',
										self.use_behavior(ActionWrapper_MoveSM, 'Return to Bar'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'actionBarman'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
