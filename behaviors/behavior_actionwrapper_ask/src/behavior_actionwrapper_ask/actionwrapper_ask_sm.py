#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_ask')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.SetRosParam import SetRosParam
from behavior_action_findperson.action_findperson_sm import Action_findPersonSM
from sara_flexbe_states.for_loop import ForLoop
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun May 27 2018
@author: Philippe La Madeleine
'''
class ActionWrapper_AskSM(Behavior):
	'''
	Ask something
	'''


	def __init__(self):
		super(ActionWrapper_AskSM, self).__init__()
		self.name = 'ActionWrapper_Ask'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_findPersonSM, 'Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 160 33 
		# ["Ask", "Question"]



	def create(self):
		# x:793 y:463, x:215 y:476, x:458 y:463
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = "Default question"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:43 y:162
			OperatableStateMachine.add('SetPerson',
										SetKey(Value="person"),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personKey'})

			# x:364 y:136
			OperatableStateMachine.add('AskTheQuestion',
										SaraSayKey(Format=lambda x: x, emotion=1, block=True),
										transitions={'done': 'GetTheResponse'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'question'})

			# x:194 y:99
			OperatableStateMachine.add('trouveLaQuestion',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'question'})

			# x:526 y:150
			OperatableStateMachine.add('GetTheResponse',
										GetSpeech(watchdog=7),
										transitions={'done': 'StoreRosParamResponse', 'nothing': 'looping', 'fail': 'looping'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'response'})

			# x:379 y:307
			OperatableStateMachine.add('NotUnderstand',
										SaraSay(sentence="Soory, I did not understand.", emotion=1, block=True),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:711 y:145
			OperatableStateMachine.add('StoreRosParamResponse',
										SetRosParam(ParamName="ResponseOfQuestion"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'response'})

			# x:30 y:275
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(Action_findPersonSM, 'Action_findPerson'),
										transitions={'done': 'fisrtSentence', 'pas_done': 'NoPerson'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'personKey', 'entity': 'entity'})

			# x:222 y:305
			OperatableStateMachine.add('NoPerson',
										SaraSay(sentence="I did not find any person. ", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:169 y:194
			OperatableStateMachine.add('fisrtSentence',
										SaraSay(sentence="Hello, I have a question for you.", emotion=1, block=True),
										transitions={'done': 'trouveLaQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:541 y:257
			OperatableStateMachine.add('looping',
										ForLoop(repeat=2),
										transitions={'do': 'NotUnderstand', 'end': 'saraSorry'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:606 y:395
			OperatableStateMachine.add('saraSorry',
										SaraSay(sentence="Sorry, I can't understand your response.", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
