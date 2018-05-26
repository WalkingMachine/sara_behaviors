#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_help_me_carry')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_receive_bag.action_receive_bag_sm import Action_Receive_BagSM
from sara_flexbe_states.get_speech import GetSpeech
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from flexbe_states.calculation_state import CalculationState
from behavior_action_follow.action_follow_sm import Action_followSM
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.set_gripper_state import SetGripperState
from flexbe_states.wait_state import WaitState
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.get_robot_pose import Get_Robot_Pose
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 19 2018
@author: Huynh-Anh Le
'''
class HelpmecarrySM(Behavior):
	'''
	Helps someone carry groceries
	'''


	def __init__(self):
		super(HelpmecarrySM, self).__init__()
		self.name = 'Help me carry'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_Receive_BagSM, 'Action_Receive_Bag')
		self.add_behavior(Action_followSM, 'Getting ready and ID Operator/Follow/Action_follow')
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 303 89 /Getting ready and ID Operator
		# Attend que l'operateur s'identifie. Le robot memorise l'identifiant. Le robot suit l'operateur.

		# O 179 806 
		# Une fois que le robot arrive a destination, il informe quil laissera le sac sur le sol.

		# O 265 23 
		# retourne a la position initiale

		# O 440 415 
		# lorsquil arrive a destination, il baisse le bras, ouvre la pince ,attend et ferme sa pince.



	def create(self):
		# x:1400 y:350, x:712 y:94, x:980 y:176
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'not_found'], input_keys=['ID'])
		_state_machine.userdata.ID = 0
		_state_machine.userdata.Closed_Gripper_Width = 1
		_state_machine.userdata.Open_Gripper_Width = 255

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:489 y:420, x:418 y:463
		_sm_ecoute_0 = OperatableStateMachine(outcomes=['arrete', 'fail'])

		with _sm_ecoute_0:
			# x:53 y:35
			OperatableStateMachine.add('Ecoute',
										GetSpeech(watchdog=5),
										transitions={'done': 'stop', 'nothing': 'Ecoute', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:373 y:215
			OperatableStateMachine.add('stop',
										RegexTester(regex=".*stop.*"),
										transitions={'true': 'arrete', 'false': 'Ecoute'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})


		# x:346 y:367, x:130 y:365, x:230 y:365, x:178 y:422, x:430 y:365
		_sm_follow_1 = ConcurrencyContainer(outcomes=['done', 'failed'], input_keys=['ID', 'distance'], conditions=[
										('failed', [('Action_follow', 'failed')]),
										('done', [('Ecoute', 'arrete')]),
										('failed', [('Ecoute', 'fail')])
										])

		with _sm_follow_1:
			# x:107 y:103
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(Action_followSM, 'Getting ready and ID Operator/Follow/Action_follow'),
										transitions={'failed': 'failed'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID', 'distance': 'distance'})

			# x:294 y:146
			OperatableStateMachine.add('Ecoute',
										_sm_ecoute_0,
										transitions={'arrete': 'done', 'fail': 'failed'},
										autonomy={'arrete': Autonomy.Inherit, 'fail': Autonomy.Inherit})


		# x:14 y:304, x:345 y:320, x:369 y:177, x:803 y:205
		_sm_getting_ready_and_id_operator_2 = OperatableStateMachine(outcomes=['false', 'failed', 'fail', 'done'])

		with _sm_getting_ready_and_id_operator_2:
			# x:62 y:46
			OperatableStateMachine.add('getSpeech',
										GetSpeech(watchdog=5),
										transitions={'done': 'UnderstandingOpe', 'nothing': 'getSpeech', 'fail': 'fail'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:133 y:308
			OperatableStateMachine.add('start',
										SaraSay(sentence="I am ready", emotion=1, block=True),
										transitions={'done': 'person'},
										autonomy={'done': Autonomy.Off})

			# x:79 y:199
			OperatableStateMachine.add('UnderstandingOpe',
										RegexTester(regex=".*follow *me.*"),
										transitions={'true': 'start', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:181 y:511
			OperatableStateMachine.add('FindId',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'GetID', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'person', 'list_entities_by_name': 'Entities_list', 'number': 'number'})

			# x:368 y:541
			OperatableStateMachine.add('GetID',
										CalculationState(calculation=lambda x: x[0].ID),
										transitions={'done': 'setID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entities_list', 'output_value': 'ID'})

			# x:582 y:323
			OperatableStateMachine.add('Follow',
										_sm_follow_1,
										transitions={'done': 'done', 'failed': 'say fail'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ID': 'ID', 'distance': 'distance'})

			# x:499 y:492
			OperatableStateMachine.add('setID',
										SetRosParam(ParamName="OperatorID"),
										transitions={'done': 'distance'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:464 y:296
			OperatableStateMachine.add('say fail',
										SaraSay(sentence="Sorry, I lost you.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:37 y:456
			OperatableStateMachine.add('person',
										SetKey(Value="person"),
										transitions={'done': 'FindId'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'person'})

			# x:659 y:462
			OperatableStateMachine.add('distance',
										SetKey(Value=1.25),
										transitions={'done': 'Follow'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})



		with _state_machine:
			# x:145 y:36
			OperatableStateMachine.add('serIdle',
										SetKey(Value="IdlePose"),
										transitions={'done': 'IDle'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:79 y:433
			OperatableStateMachine.add('PutBAg',
										SaraSay(sentence="Could you put the bag in my hand?, please", emotion=1, block=True),
										transitions={'done': 'Action_Receive_Bag'},
										autonomy={'done': Autonomy.Off})

			# x:161 y:490
			OperatableStateMachine.add('Action_Receive_Bag',
										self.use_behavior(Action_Receive_BagSM, 'Action_Receive_Bag'),
										transitions={'finished': 'bringit', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Closed_Gripper_Width': 'Closed_Gripper_Width', 'Open_Gripper_Width': 'Open_Gripper_Width', 'Closed_Gripper_Width': 'Closed_Gripper_Width'})

			# x:290 y:606
			OperatableStateMachine.add('Arrived',
										SaraSay(sentence="I have food, people. I will drop the bags on the floor.", emotion=1, block=True),
										transitions={'done': 'levelDrop'},
										autonomy={'done': Autonomy.Off})

			# x:196 y:232
			OperatableStateMachine.add('Getting ready and ID Operator',
										_sm_getting_ready_and_id_operator_2,
										transitions={'false': 'Getting ready and ID Operator', 'failed': 'failed', 'fail': 'failed', 'done': 'sac'},
										autonomy={'false': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'fail': Autonomy.Inherit, 'done': Autonomy.Inherit})

			# x:52 y:235
			OperatableStateMachine.add('getspeech2',
										GetSpeech(watchdog=5),
										transitions={'done': 'takebag', 'nothing': 'getspeech2', 'fail': 'failed'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:49 y:302
			OperatableStateMachine.add('takebag',
										RegexTester(regex=".*((take)|(bag)|(ready)).*"),
										transitions={'true': 'askforbags', 'false': 'getspeech2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'text': 'words', 'result': 'result'})

			# x:561 y:608
			OperatableStateMachine.add('dropbag',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'Open', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Idle'})

			# x:702 y:612
			OperatableStateMachine.add('Open',
										SetGripperState(width=0.1, effort=1),
										transitions={'object': 'wait', 'no_object': 'failed'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:1012 y:614
			OperatableStateMachine.add('close',
										SetGripperState(width=0, effort=1),
										transitions={'object': 'returnIdl', 'no_object': 'returnIdl'},
										autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
										remapping={'object_size': 'object_size'})

			# x:879 y:614
			OperatableStateMachine.add('wait',
										WaitState(wait_time=5),
										transitions={'done': 'close'},
										autonomy={'done': Autonomy.Off})

			# x:418 y:609
			OperatableStateMachine.add('levelDrop',
										SetKey(Value="IdlePose"),
										transitions={'done': 'dropbag'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Idle'})

			# x:69 y:164
			OperatableStateMachine.add('sac',
										SaraSay(sentence="Tell me, when you are ready", emotion=1, block=True),
										transitions={'done': 'getspeech2'},
										autonomy={'done': Autonomy.Off})

			# x:1172 y:615
			OperatableStateMachine.add('returnIdl',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'done', 'failed': 'returnIdl'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'Idle'})

			# x:1301 y:611
			OperatableStateMachine.add('done',
										SaraSay(sentence="You are welcome,have a nice day", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:37 y:528
			OperatableStateMachine.add('bringit',
										SaraSay(sentence="I will bring it inside", emotion=1, block=True),
										transitions={'done': 'setrelative'},
										autonomy={'done': Autonomy.Off})

			# x:124 y:617
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'Arrived', 'failed': 'Action_Move'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'PoseOrigin', 'relative': 'relative'})

			# x:17 y:623
			OperatableStateMachine.add('setrelative',
										SetKey(Value=False),
										transitions={'done': 'Action_Move'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:59 y:367
			OperatableStateMachine.add('askforbags',
										SaraSay(sentence="I will gladly take your bags", emotion=1, block=True),
										transitions={'done': 'PutBAg'},
										autonomy={'done': Autonomy.Off})

			# x:251 y:54
			OperatableStateMachine.add('IDle',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'get_pose', 'failed': 'get_pose'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:86 y:111
			OperatableStateMachine.add('get_pose',
										Get_Robot_Pose(),
										transitions={'done': 'Getting ready and ID Operator'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'PoseOrigin'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
