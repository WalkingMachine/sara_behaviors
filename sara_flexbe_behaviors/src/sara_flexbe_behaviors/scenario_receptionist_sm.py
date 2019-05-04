#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM as sara_flexbe_behaviors__Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM as sara_flexbe_behaviors__Action_findPersonSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_nlu_receptionist import SaraNLUreceptionist
from sara_flexbe_states.door_detector import DoorDetector
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Apr 27 2019
@author: Quentin Gaillot
'''
class Scenario_ReceptionistSM(Behavior):
	'''
	Scenario receptionist 2019 (Party Host)
	'''


	def __init__(self):
		super(Scenario_ReceptionistSM, self).__init__()
		self.name = 'Scenario_Receptionist'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Knowing John/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Knowing John/Action_findPerson')
		self.add_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome and introduce Guest1/Action_Move')
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome and introduce Guest1/Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:870 y:688, x:860 y:224
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.personAlreadyInLocation = "living room"
		_state_machine.userdata.personAlreadyInName = "John"
		_state_machine.userdata.personAlreadyInDrink = "coke"
		_state_machine.userdata.entranceLocation = "front door"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_welcome_and_intruduce_guest2_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['Guest1Drink', 'personAlreadyInName', 'personAlreadyInDrink', 'personAlreadyInLocation', 'entranceLocation', 'Guest1Name', 'Guest1Entity'], output_keys=['Guest2Drink', 'Guest2Name'])

		with _sm_welcome_and_intruduce_guest2_0:
			# x:30 y:40
			OperatableStateMachine.add('say3',
										SaraSay(sentence="say", input_keys=[], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:1393 y:774, x:1254 y:36
		_sm_welcome_and_introduce_guest1_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personAlreadyInDrink', 'personAlreadyInName', 'entranceLocation', 'personAlreadyInLocation'], output_keys=['Guest1Drink', 'Guest1Name', 'Guest1Entity'])

		with _sm_welcome_and_introduce_guest1_1:
			# x:95 y:34
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'welcome and introduce Guest1/Action_Move'),
										transitions={'finished': 'say help to open the door', 'failed': 'retry moving'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'entranceLocation'})

			# x:294 y:35
			OperatableStateMachine.add('retry moving',
										ForLoop(repeat=1),
										transitions={'do': 'Action_Move', 'end': 'say cannot do task'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:555 y:35
			OperatableStateMachine.add('say cannot do task',
										SaraSay(sentence="I failed to do my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'set G1 name to unknown'},
										autonomy={'done': Autonomy.Off})

			# x:109 y:212
			OperatableStateMachine.add('check if door is open',
										DoorDetector(timeout=12),
										transitions={'done': 'Action_findPerson', 'failed': 'retry opening door'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:100 y:131
			OperatableStateMachine.add('say help to open the door',
										SaraSay(sentence="Can someone help me and open this door?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'check if door is open'},
										autonomy={'done': Autonomy.Off})

			# x:275 y:163
			OperatableStateMachine.add('retry opening door',
										ForLoop(repeat=1),
										transitions={'do': 'say help to open the door', 'end': 'say cannot do task'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:104 y:294
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'welcome and introduce Guest1/Action_findPerson', default_keys=['className']),
										transitions={'done': 'ask name G1', 'pas_done': 'say cannot do task'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'className', 'entity': 'Guest1Entity'})

			# x:707 y:34
			OperatableStateMachine.add('set G1 name to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 drink to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Name'})

			# x:866 y:30
			OperatableStateMachine.add('set G1 drink to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'set G1 entity to unknown'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Drink'})

			# x:1043 y:30
			OperatableStateMachine.add('set G1 entity to unknown',
										SetKey(Value="unknown"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Guest1Entity'})

			# x:113 y:374
			OperatableStateMachine.add('ask name G1',
										SaraSay(sentence="Hello, I am receptionist robot. What is your name?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'get name G1'},
										autonomy={'done': Autonomy.Off})

			# x:103 y:464
			OperatableStateMachine.add('get name G1',
										GetSpeech(watchdog=6),
										transitions={'done': 'nlu receptionist for name G1', 'nothing': 'retry ask name G1', 'fail': 'retry ask name G1'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:311 y:469
			OperatableStateMachine.add('retry ask name G1',
										ForLoop(repeat=2),
										transitions={'do': 'repeat ask name G1', 'end': 'finished'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index1'})

			# x:260 y:390
			OperatableStateMachine.add('repeat ask name G1',
										SaraSay(sentence="I did not understand your name. Can you repeat please?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'get name G1'},
										autonomy={'done': Autonomy.Off})

			# x:85 y:543
			OperatableStateMachine.add('nlu receptionist for name G1',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'retry ask name G1'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'answer': 'Guest1Name'})


		# x:755 y:735, x:1041 y:194
		_sm_knowing_john_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['location', 'personAlreadyIn'], output_keys=['JohnDrink'])

		with _sm_knowing_john_2:
			# x:69 y:29
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(sara_flexbe_behaviors__Action_MoveSM, 'Knowing John/Action_Move'),
										transitions={'finished': 'Action_findPerson', 'failed': 'SayFailed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'location'})

			# x:79 y:197
			OperatableStateMachine.add('say',
										SaraSay(sentence="Hello John! What is your favorite drink", input_keys=[], emotion=0, block=True),
										transitions={'done': 'listenToJohn'},
										autonomy={'done': Autonomy.Off})

			# x:67 y:115
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Knowing John/Action_findPerson'),
										transitions={'done': 'say', 'pas_done': 'SayFailed'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'personAlreadyIn', 'entity': 'entityJohn'})

			# x:864 y:174
			OperatableStateMachine.add('setDrinkToUnknown',
										SetKey(Value="Unknown"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'JohnDrink'})

			# x:80 y:315
			OperatableStateMachine.add('listenToJohn',
										GetSpeech(watchdog=4),
										transitions={'done': 'understanding john', 'nothing': 'AskToRepeatOneTime', 'fail': 'AskToRepeatOneTime'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'sentence'})

			# x:329 y:292
			OperatableStateMachine.add('AskToRepeatOneTime',
										ForLoop(repeat=2),
										transitions={'do': 'LastChanceToGetTheDrink', 'end': 'SayFailed'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:210 y:197
			OperatableStateMachine.add('LastChanceToGetTheDrink',
										SaraSay(sentence="I did not understand. What is your favorite drink?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'listenToJohn'},
										autonomy={'done': Autonomy.Off})

			# x:707 y:172
			OperatableStateMachine.add('SayFailed',
										SaraSay(sentence="Sorry, I failed my task.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'setDrinkToUnknown'},
										autonomy={'done': Autonomy.Off})

			# x:87 y:477
			OperatableStateMachine.add('understanding john',
										SaraNLUreceptionist(),
										transitions={'understood': 'finished', 'fail': 'AskToRepeatOneTime'},
										autonomy={'understood': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'sentence': 'sentence', 'answer': 'JohnDrink'})



		with _state_machine:
			# x:1415 y:45
			OperatableStateMachine.add('Knowing John',
										_sm_knowing_john_2,
										transitions={'finished': 'welcome and introduce Guest1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'location': 'personAlreadyInLocation', 'personAlreadyIn': 'personAlreadyInName', 'JohnDrink': 'JohnDrink'})

			# x:175 y:137
			OperatableStateMachine.add('welcome and introduce Guest1',
										_sm_welcome_and_introduce_guest1_1,
										transitions={'finished': 'Welcome and intruduce Guest2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personAlreadyInDrink': 'personAlreadyInDrink', 'personAlreadyInName': 'personAlreadyInName', 'entranceLocation': 'entranceLocation', 'personAlreadyInLocation': 'personAlreadyInLocation', 'Guest1Drink': 'Guest1Drink', 'Guest1Name': 'Guest1Name', 'Guest1Entity': 'Guest1Entity'})

			# x:168 y:391
			OperatableStateMachine.add('Welcome and intruduce Guest2',
										_sm_welcome_and_intruduce_guest2_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Guest1Drink': 'Guest1Drink', 'personAlreadyInName': 'personAlreadyInName', 'personAlreadyInDrink': 'personAlreadyInDrink', 'personAlreadyInLocation': 'personAlreadyInLocation', 'entranceLocation': 'entranceLocation', 'Guest1Name': 'Guest1Name', 'Guest1Entity': 'Guest1Entity', 'Guest2Drink': 'Guest2Drink', 'Guest2Name': 'Guest2Name'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
