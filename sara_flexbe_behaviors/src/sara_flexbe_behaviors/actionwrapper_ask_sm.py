#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_findperson_sm import Action_findPersonSM as sara_flexbe_behaviors__Action_findPersonSM
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.SetRosParamKey import SetRosParamKey
from flexbe_states.log_key_state import LogKeyState
from sara_flexbe_states.SetRosParam import SetRosParam
from flexbe_states.check_condition_state import CheckConditionState
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
		self.add_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Action_findPerson')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 160 33 
		# ["Ask", "Question", "RosParamName"]



	def create(self):
		# x:808 y:575, x:78 y:552, x:477 y:566
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Ask", "How are you today?", "Answer"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:675 y:219, x:771 y:50
		_sm_confirm_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['answer'])

		with _sm_confirm_0:
			# x:70 y:60
			OperatableStateMachine.add('Heard',
										SaraSay(sentence=lambda x: "I heard "+x+". Is that correct?", input_keys=[], emotion=0, block=True),
										transitions={'done': 'get speech'},
										autonomy={'done': Autonomy.Off})

			# x:501 y:98
			OperatableStateMachine.add('check yes',
										CheckConditionState(predicate=lambda x: "yes" in x and not "no" in x),
										transitions={'true': 'finished', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})

			# x:259 y:92
			OperatableStateMachine.add('get speech',
										GetSpeech(watchdog=5),
										transitions={'done': 'check yes', 'nothing': 'failed', 'fail': 'finished'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})



		with _state_machine:
			# x:43 y:162
			OperatableStateMachine.add('SetPerson',
										SetKey(Value="person"),
										transitions={'done': 'Action_findPerson'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personKey'})

			# x:194 y:99
			OperatableStateMachine.add('trouveLaQuestion',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'question'})

			# x:545 y:161
			OperatableStateMachine.add('GetTheResponse',
										GetSpeech(watchdog=7),
										transitions={'done': 'Confirm', 'nothing': 'looping', 'fail': 'looping'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'response'})

			# x:372 y:262
			OperatableStateMachine.add('NotUnderstand',
										SaraSay(sentence="Soory, I did not understand.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'AskTheQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:23 y:285
			OperatableStateMachine.add('Action_findPerson',
										self.use_behavior(sara_flexbe_behaviors__Action_findPersonSM, 'Action_findPerson'),
										transitions={'done': 'fisrtSentence', 'pas_done': 'NoPerson'},
										autonomy={'done': Autonomy.Inherit, 'pas_done': Autonomy.Inherit},
										remapping={'className': 'personKey', 'entity': 'entity'})

			# x:224 y:301
			OperatableStateMachine.add('NoPerson',
										SaraSay(sentence="I did not find any person. ", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause1'},
										autonomy={'done': Autonomy.Off})

			# x:169 y:194
			OperatableStateMachine.add('fisrtSentence',
										SaraSay(sentence="Hello, I have a question for you.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'trouveLaQuestion'},
										autonomy={'done': Autonomy.Off})

			# x:539 y:332
			OperatableStateMachine.add('looping',
										ForLoop(repeat=2),
										transitions={'do': 'NotUnderstand', 'end': 'saraSorry'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:540 y:473
			OperatableStateMachine.add('saraSorry',
										SaraSay(sentence="Sorry, I can't understand your response.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause2'},
										autonomy={'done': Autonomy.Off})

			# x:776 y:209
			OperatableStateMachine.add('getRosparmName',
										CalculationState(calculation=lambda x: x[2]),
										transitions={'done': 'SetRosParamKey'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'RosParamName'})

			# x:778 y:301
			OperatableStateMachine.add('SetRosParamKey',
										SetRosParamKey(),
										transitions={'done': 'log'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'response', 'ParamName': 'RosParamName'})

			# x:787 y:482
			OperatableStateMachine.add('thank you',
										SaraSay(sentence="Thank you for your answer.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:789 y:390
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'thank you'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'response'})

			# x:221 y:384
			OperatableStateMachine.add('cause1',
										SetKey(Value="I didn't find any person"),
										transitions={'done': 'set cause failure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:326 y:503
			OperatableStateMachine.add('cause2',
										SetKey(Value="I did not understand the answer"),
										transitions={'done': 'set cause failure'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:159 y:468
			OperatableStateMachine.add('set cause failure',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:769 y:88
			OperatableStateMachine.add('Confirm',
										_sm_confirm_0,
										transitions={'finished': 'getRosparmName', 'failed': 'AskTheQuestion'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'answer': 'response'})

			# x:367 y:117
			OperatableStateMachine.add('AskTheQuestion',
										SaraSay(sentence=lambda x: x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'GetTheResponse'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
