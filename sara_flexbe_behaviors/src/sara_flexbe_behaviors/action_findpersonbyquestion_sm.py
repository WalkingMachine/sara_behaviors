#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.init_sequence_sm import Init_SequenceSM as Init_SequenceSM
from sara_flexbe_states.for_loop_with_input import ForLoopWithInput
from flexbe_states.wait_state import WaitState
from sara_flexbe_behaviors.action_ask_sm import Action_AskSM as Action_AskSM
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.decision_state import DecisionState
from sara_flexbe_behaviors.action_turn_sm import action_turnSM as action_turnSM
from sara_flexbe_states.FilterKey import FilterKey
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from sara_flexbe_states.FIFO_Add import FIFO_Add
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_set_head_angle_key import SaraSetHeadAngleKey
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.Get_direction_to_point import Get_direction_to_point
from sara_flexbe_states.FIFO_New import FIFO_New
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
		self.add_behavior(Init_SequenceSM, 'Init_Sequence')
		self.add_behavior(Action_AskSM, 'ask while looking at person/ask/Action_Ask')
		self.add_behavior(action_turnSM, 'tourne tete et base/action_turn')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:860 y:786, x:837 y:171, x:828 y:43
		_state_machine = OperatableStateMachine(outcomes=['found', 'failed', 'not_found'], input_keys=['question'], output_keys=['entityFound'])
		_state_machine.userdata.question = ""
		_state_machine.userdata.entityFound = ""
		_state_machine.userdata.personKey = "person"
		_state_machine.userdata.index = -1
		_state_machine.userdata.rotation180degres = -3.14

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
										WaitState(wait_time=3),
										transitions={'done': 'Action_Ask'},
										autonomy={'done': Autonomy.Off})

			# x:46 y:155
			OperatableStateMachine.add('Action_Ask',
										self.use_behavior(Action_AskSM, 'ask while looking at person/ask/Action_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'question': 'question', 'answer': 'answer'})


		# x:871 y:712, x:874 y:127
		_sm_get_real_id_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['entity', 'personKey', 'FIFO'], output_keys=['personID'])

		with _sm_get_real_id_2:
			# x:47 y:32
			OperatableStateMachine.add('get posittion face or entity',
										CalculationState(calculation=lambda x: x.face.boundingBox.Center if x.face.id != '' else x.position),
										transitions={'done': 'get direction to point'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'entity', 'output_value': 'pointToLook'})

			# x:27 y:351
			OperatableStateMachine.add('look at point',
										SaraSetHeadAngleKey(),
										transitions={'done': 'wait 1'},
										autonomy={'done': Autonomy.Off},
										remapping={'yaw': 'yaw', 'pitch': 'pitch'})

			# x:40 y:423
			OperatableStateMachine.add('wait 1',
										WaitState(wait_time=1),
										transitions={'done': 'list entity in front'},
										autonomy={'done': Autonomy.Off})

			# x:24 y:491
			OperatableStateMachine.add('list entity in front',
										list_entities_by_name(frontality_level=0.5, distance_max=3),
										transitions={'found': 'fitler the entity list to remove id already checked', 'none_found': 'set key'},
										autonomy={'found': Autonomy.Off, 'none_found': Autonomy.Off},
										remapping={'name': 'personKey', 'entity_list': 'entity_list', 'number': 'number'})

			# x:42 y:632
			OperatableStateMachine.add('calcul first entity ID',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'say real id'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'filteredEntityList', 'output_value': 'personID'})

			# x:518 y:578
			OperatableStateMachine.add('say real id',
										SaraSay(sentence=lambda x: "The real ID is "+str(x[0])+".", input_keys=["personID"], emotion=0, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'personID': 'personID'})

			# x:539 y:164
			OperatableStateMachine.add('set key',
										SetKey(Value=0),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'personID'})

			# x:34 y:234
			OperatableStateMachine.add('pitch to 0.1 if no face',
										FlexibleCalculationState(calculation=lambda x: x[0] if x[1].face.id != '' else 0.1, input_keys=["pitch", "entity"]),
										transitions={'done': 'look at point'},
										autonomy={'done': Autonomy.Off},
										remapping={'pitch': 'pitch', 'entity': 'entity', 'output_value': 'pitch'})

			# x:37 y:149
			OperatableStateMachine.add('get direction to point',
										Get_direction_to_point(frame_origin="base_link", frame_reference="head_link"),
										transitions={'done': 'pitch to 0.1 if no face', 'fail': 'set key'},
										autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'targetPoint': 'pointToLook', 'yaw': 'yaw', 'pitch': 'pitch'})

			# x:29 y:560
			OperatableStateMachine.add('fitler the entity list to remove id already checked',
										FilterKey(filter_function=lambda x: x[0].ID not in x[1], input_keys=["input_list", "FIFO"]),
										transitions={'not_empty': 'calcul first entity ID', 'empty': 'set key'},
										autonomy={'not_empty': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'entity_list', 'FIFO': 'FIFO', 'output_list': 'filteredEntityList'})


		# x:30 y:458, x:710 y:24
		_sm_tourne_tete_et_base_3 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['index', 'rotation180degres'])

		with _sm_tourne_tete_et_base_3:
			# x:57 y:27
			OperatableStateMachine.add('decide',
										DecisionState(outcomes=["_0", "_1", "_2", "_3", "_4"], conditions=lambda x: "_"+str(x)),
										transitions={'_0': 'look center', '_1': 'look center_2', '_2': 'look center_3', '_3': 'action_turn', '_4': 'look center_5'},
										autonomy={'_0': Autonomy.Off, '_1': Autonomy.Off, '_2': Autonomy.Off, '_3': Autonomy.Off, '_4': Autonomy.Off},
										remapping={'input_value': 'index'})

			# x:186 y:236
			OperatableStateMachine.add('look right',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'wait right'},
										autonomy={'done': Autonomy.Off})

			# x:208 y:307
			OperatableStateMachine.add('wait right',
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:322 y:109
			OperatableStateMachine.add('look center_3',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait center_3'},
										autonomy={'done': Autonomy.Off})

			# x:325 y:174
			OperatableStateMachine.add('wait center_3',
										WaitState(wait_time=3),
										transitions={'done': 'look right_2'},
										autonomy={'done': Autonomy.Off})

			# x:318 y:240
			OperatableStateMachine.add('look right_2',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'wait right_2'},
										autonomy={'done': Autonomy.Off})

			# x:345 y:310
			OperatableStateMachine.add('wait right_2',
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:489 y:178
			OperatableStateMachine.add('look left_2_2',
										SaraSetHeadAngle(pitch=0.1, yaw=1.5),
										transitions={'done': 'waitleft_2_2'},
										autonomy={'done': Autonomy.Off})

			# x:506 y:247
			OperatableStateMachine.add('waitleft_2_2',
										WaitState(wait_time=3),
										transitions={'done': 'look center_4'},
										autonomy={'done': Autonomy.Off})

			# x:501 y:319
			OperatableStateMachine.add('look center_4',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait center_4'},
										autonomy={'done': Autonomy.Off})

			# x:520 y:407
			OperatableStateMachine.add('wait center_4',
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:476 y:109
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'tourne tete et base/action_turn'),
										transitions={'finished': 'look left_2_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'rotation180degres'})

			# x:199 y:108
			OperatableStateMachine.add('look center_2',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait center_2'},
										autonomy={'done': Autonomy.Off})

			# x:51 y:113
			OperatableStateMachine.add('look center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait center'},
										autonomy={'done': Autonomy.Off})

			# x:56 y:174
			OperatableStateMachine.add('wait center',
										WaitState(wait_time=4),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})

			# x:206 y:173
			OperatableStateMachine.add('wait center_2',
										WaitState(wait_time=2),
										transitions={'done': 'look right'},
										autonomy={'done': Autonomy.Off})

			# x:730 y:110
			OperatableStateMachine.add('look center_5',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'wait center_5'},
										autonomy={'done': Autonomy.Off})

			# x:741 y:193
			OperatableStateMachine.add('wait center_5',
										WaitState(wait_time=3),
										transitions={'done': 'look right_5'},
										autonomy={'done': Autonomy.Off})

			# x:733 y:296
			OperatableStateMachine.add('look right_5',
										SaraSetHeadAngle(pitch=0.1, yaw=-1.5),
										transitions={'done': 'wait right_5'},
										autonomy={'done': Autonomy.Off})

			# x:731 y:422
			OperatableStateMachine.add('wait right_5',
										WaitState(wait_time=3),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:449 y:45, x:454 y:135, x:447 y:195, x:446 y:252, x:430 y:458, x:530 y:458
		_sm_ask_while_looking_at_person_4 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['personID', 'question'], output_keys=['answer'], conditions=[
										('finished', [('ask', 'finished')]),
										('failed', [('ask', 'failed')]),
										('finished', [('keep looking at person', 'finished')]),
										('failed', [('keep looking at person', 'failed')])
										])

		with _sm_ask_while_looking_at_person_4:
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
			# x:30 y:115
			OperatableStateMachine.add('Init_Sequence',
										self.use_behavior(Init_SequenceSM, 'Init_Sequence'),
										transitions={'finished': 'create fifo', 'failed': 'create fifo'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:164 y:62
			OperatableStateMachine.add('for loop',
										ForLoopWithInput(repeat=4),
										transitions={'do': 'tourne tete et base', 'end': 'not_found'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index_in': 'index', 'index_out': 'index'})

			# x:260 y:557
			OperatableStateMachine.add('ask while looking at person',
										_sm_ask_while_looking_at_person_4,
										transitions={'finished': 'answer contains yes', 'failed': 'add id'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'personID': 'personID', 'question': 'question', 'answer': 'answer'})

			# x:289 y:480
			OperatableStateMachine.add('get personID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'ask while looking at person'},
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

			# x:372 y:89
			OperatableStateMachine.add('tourne tete et base',
										_sm_tourne_tete_et_base_3,
										transitions={'done': 'get list of person', 'failed': 'not_found'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'index': 'index', 'rotation180degres': 'rotation180degres'})

			# x:263 y:322
			OperatableStateMachine.add('fitler the entity list to remove id already checked',
										FilterKey(filter_function=lambda x: x[0].ID not in x[1], input_keys=["input_list", "FIFO"]),
										transitions={'not_empty': 'get first entity', 'empty': 'look center'},
										autonomy={'not_empty': Autonomy.Off, 'empty': Autonomy.Off},
										remapping={'input_list': 'entityList', 'FIFO': 'FIFO', 'output_list': 'filteredEntityList'})

			# x:268 y:388
			OperatableStateMachine.add('get first entity',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'get real id'},
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

			# x:472 y:438
			OperatableStateMachine.add('get real id',
										_sm_get_real_id_2,
										transitions={'finished': 'ask while looking at person', 'failed': 'get personID'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'entity': 'personEntity', 'personKey': 'personKey', 'FIFO': 'FIFO', 'personID': 'personID'})

			# x:35 y:53
			OperatableStateMachine.add('create fifo',
										FIFO_New(),
										transitions={'done': 'for loop'},
										autonomy={'done': Autonomy.Off},
										remapping={'FIFO': 'FIFO'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
