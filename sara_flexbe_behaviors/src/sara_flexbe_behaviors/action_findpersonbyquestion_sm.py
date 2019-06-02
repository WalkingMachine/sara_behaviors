#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.FIFO_New import FIFO_New
from sara_flexbe_states.for_loop_with_input import ForLoopWithInput
from flexbe_states.wait_state import WaitState
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as sara_flexbe_behaviors__Action_AskSM
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as sara_flexbe_behaviors__action_turnSM
from sara_flexbe_states.FilterKey import FilterKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.FIFO_Add import FIFO_Add
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.log_key_state import LogKeyState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 01 2019
@author: Quentin Gaillot
'''
class Action_FindPersonByQuestionSM(Behavior):
	'''
	Find a person by asking a question and return an entity (ex: Are you John?)
Look 180 degres, do not rotate
	'''


	def __init__(self):
		super(Action_FindPersonByQuestionSM, self).__init__()
		self.name = 'Action_FindPersonByQuestion'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask while looking at person/ask/Action_Ask')
		self.add_behavior(sara_flexbe_behaviors__action_turnSM, 'tourne tete et base/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:860 y:786, x:837 y:171, x:828 y:43
		_state_machine = OperatableStateMachine(outcomes=['found', 'failed', 'not_found'], input_keys=['question'], output_keys=['entityFound'])
		_state_machine.userdata.question = "Are you Philippe?"
		_state_machine.userdata.entityFound = ""
		_state_machine.userdata.personKey = "person"
		_state_machine.userdata.index = -1
		_state_machine.userdata.rotation90degres = -1.57

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:458, x:130 y:458
		_sm_keep_looking_at_person_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['personID'])

		with _sm_keep_looking_at_person_0:
			# x:79 y:77
			OperatableStateMachine.add('keep looking',
										KeepLookingAt(),
										transitions={'failed': 'keep looking'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'personID'})


		# x:30 y:458, x:130 y:458
		_sm_ask_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['question'], output_keys=['answer'])

		with _sm_ask_1:
			# x:57 y:66
			OperatableStateMachine.add('wait',
										WaitState(wait_time=5),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off})

			# x:46 y:155
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(sara_flexbe_behaviors__Action_AskSM, 'ask while looking at person/ask/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})


		# x:30 y:458, x:572 y:96
		_sm_tourne_tete_et_base_2 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['rotation90degres', 'index'])

		with _sm_tourne_tete_et_base_2:
			# x:30 y:57
			OperatableStateMachine.add('if index is 0',
										CheckConditionState(predicate=lambda x: x == 0),
										transitions={'true': 'look left', 'false': 'if index is 1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'index'})

			# x:56 y:187
			OperatableStateMachine.add('waitleft',
										WaitState(wait_time=4),
										transitions={'done': 'look right'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:244
			OperatableStateMachine.add('look right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'wait right'},
										autonomy={'done': Autonomy.Off})

			# x:53 y:309
			OperatableStateMachine.add('wait right',
										WaitState(wait_time=6),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:171 y:127
			OperatableStateMachine.add('look left_2',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'waitleft_2'},
										autonomy={'done': Autonomy.Off})

			# x:177 y:186
			OperatableStateMachine.add('waitleft_2',
										WaitState(wait_time=4),
										transitions={'done': 'look right_2'},
										autonomy={'done': Autonomy.Off})

			# x:169 y:245
			OperatableStateMachine.add('look right_2',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'wait right_2'},
										autonomy={'done': Autonomy.Off})

			# x:171 y:306
			OperatableStateMachine.add('wait right_2',
										WaitState(wait_time=6),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:312 y:182
			OperatableStateMachine.add('look left_2_2',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'waitleft_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:323 y:243
			OperatableStateMachine.add('waitleft_2_2',
										WaitState(wait_time=6),
										transitions={'done': 'look right_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:306 y:303
			OperatableStateMachine.add('look right_2_2',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'wait right_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:316 y:364
			OperatableStateMachine.add('wait right_2_2',
										WaitState(wait_time=6),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:294 y:114
			OperatableStateMachine.add('action_turn',
										self.use_behavior(sara_flexbe_behaviors__action_turnSM, 'tourne tete et base/action_turn'),
										transitions={'finished': 'look left_2_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation90degres'})

			# x:218 y:40
			OperatableStateMachine.add('if index is 1',
										CheckConditionState(predicate=lambda x: x == 1),
										transitions={'true': 'look left_2', 'false': 'action_turn'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'index'})

			# x:40 y:126
			OperatableStateMachine.add('look left',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'waitleft'},
										autonomy={'done': Autonomy.Off})


		# x:449 y:45, x:454 y:135, x:447 y:195, x:446 y:252, x:430 y:458, x:530 y:458
		_sm_ask_while_looking_at_person_3 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID', 'question'], output_keys=['answer'], conditions=[
										('finished', [('ask', 'finished')]),
										('failed', [('ask', 'failed')]),
										('finished', [('keep looking at person', 'finished')]),
										('failed', [('keep looking at person', 'failed')])
										])

		with _sm_ask_while_looking_at_person_3:
			# x:97 y:55
			OperatableStateMachine.add('ask',
										_sm_ask_1,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})

			# x:65 y:197
			OperatableStateMachine.add('keep looking at person',
										_sm_keep_looking_at_person_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID'})



		with _state_machine:
			# x:35 y:53
			OperatableStateMachine.add('create fifo',
										FIFO_New(),
										transitions={'done': 'for loop'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'FIFO'})

			# x:163 y:58
			OperatableStateMachine.add('for loop',
										ForLoopWithInput(repeat=3),
										transitions={'do': 'get list of person', 'end': 'not_found'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index_in': 'index', 'index_out': 'index'})

			# x:250 y:530
			OperatableStateMachine.add('ask while looking at person',
										_sm_ask_while_looking_at_person_3,
										transitions={'finished': 'answer contains yes', 'failed': 'add id'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID', 'question': 'question', 'answer': 'answer'})

			# x:269 y:461
			OperatableStateMachine.add('get personID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'log_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'personEntity', 'output_value': 'personID'})

			# x:270 y:643
			OperatableStateMachine.add('answer contains yes',
										RegexTester(regex=".*((yes)|(Yes)|(yep)|(sure)|(of course)).*"),
										transitions={'true': 'say ty', 'false': 'add id'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'answer', 'result': 'result'})

			# x:173 y:260
			OperatableStateMachine.add('look center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'for loop'},
										autonomy={'done': Autonomy.Off})

			# x:299 y:88
			OperatableStateMachine.add('tourne tete et base',
										_sm_tourne_tete_et_base_2,
										transitions={'done': 'get list of person', 'failed': 'not_found'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation90degres': 'rotation90degres', 'index': 'index'})

			# x:263 y:322
			OperatableStateMachine.add('fitler the entity list to remove id already checked',
										FilterKey(filter_function=lambda x: x[0].ID not in x[1], input_keys=["input_list", "FIFO"]),
										transitions={'not_empty': 'get first entity', 'empty': 'look center'},
										autonomy={'not_empty': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'entityList', 'FIFO': 'FIFO', 'output_list': 'filteredEntityList'})

			# x:268 y:388
			OperatableStateMachine.add('get first entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'get personID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'filteredEntityList', 'output_value': 'personEntity'})

			# x:296 y:168
			OperatableStateMachine.add('get list of person',
										list_entities_by_name(frontality_level=0.5, distance_max=3),
										transitions={'found': 'fitler the entity list to remove id already checked', 'none_found': 'for loop'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'personKey', 'entity_list': 'entityList', 'number': 'numberOfEntity'})

			# x:111 y:533
			OperatableStateMachine.add('add id',
										FIFO_Add(),
										transitions={'done': 'say keep looking'},
										autonomy={'done': Autonomy.Off},
										remapping={'Entry': 'personID', 'FIFO': 'FIFO'})

			# x:609 y:651
			OperatableStateMachine.add('say ty',
										SaraSay(sentence="Thank you.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'found'},
										autonomy={'done': Autonomy.Off})

			# x:113 y:386
			OperatableStateMachine.add('say keep looking',
										SaraSay(sentence="Ok, never mind.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'for loop'},
										autonomy={'done': Autonomy.Off})

			# x:521 y:445
			OperatableStateMachine.add('log_2',
										LogKeyState(text="personID: {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'ask while looking at person'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'personID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
