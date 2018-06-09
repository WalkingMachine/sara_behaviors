#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_spr')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
from behavior_action_turn.action_turn_sm import action_turnSM
from behavior_wonderlandsaveallpersons.wonderlandsaveallpersons_sm import WonderlandSaveAllPersonsSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 07 2018
@author: Lucas Maurice
'''
class Scenario_SPRSM(Behavior):
	'''
	Contient le scénario SPR
	'''


	def __init__(self):
		super(Scenario_SPRSM, self).__init__()
		self.name = 'Scenario_SPR'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(action_turnSM, 'Waiting And Turn/action_turn')
		self.add_behavior(WonderlandSaveAllPersonsSM, 'Analyse Crowd/Analyse/WonderlandSaveAllPersons')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1089 y:92, x:484 y:623
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.half_turn = 3.1416

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:1182 y:163
		_sm_rotate_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_rotate_0:
			# x:103 y:61
			OperatableStateMachine.add('Look Left',
										SaraSetHeadAngle(pitch=0.1, yaw=0.785),
										transitions={'done': 'Rotate Left'},
										autonomy={'done': Autonomy.Off})

			# x:495 y:60
			OperatableStateMachine.add('Look Right',
										SaraSetHeadAngle(pitch=0.1, yaw=-0.785),
										transitions={'done': 'Rotate Right'},
										autonomy={'done': Autonomy.Off})

			# x:325 y:61
			OperatableStateMachine.add('Rotate Left',
										WaitState(wait_time=4),
										transitions={'done': 'Look Right'},
										autonomy={'done': Autonomy.Off})

			# x:721 y:60
			OperatableStateMachine.add('Rotate Right',
										WaitState(wait_time=8),
										transitions={'done': 'Look Center'},
										autonomy={'done': Autonomy.Off})

			# x:945 y:60
			OperatableStateMachine.add('Look Center',
										SaraSetHeadAngle(pitch=0.1, yaw=0),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458
		_sm_analyse_1 = OperatableStateMachine(outcomes=['finished'])

		with _sm_analyse_1:
			# x:106 y:51
			OperatableStateMachine.add('WonderlandSaveAllPersons',
										self.use_behavior(WonderlandSaveAllPersonsSM, 'Analyse Crowd/Analyse/WonderlandSaveAllPersons'),
										transitions={'done': 'Wait', 'none': 'Wait'},
										autonomy={'done': Autonomy.Inherit, 'none': Autonomy.Inherit},
										remapping={'females': 'females', 'males': 'males', 'number': 'number'})

			# x:433 y:53
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=2),
										transitions={'done': 'WonderlandSaveAllPersons'},
										autonomy={'done': Autonomy.Off})


		# x:485 y:49, x:480 y:193, x:230 y:458
		_sm_analyse_crowd_2 = ConcurrencyContainer(outcomes=['finished'], conditions=[
										('finished', [('Analyse', 'finished')]),
										('finished', [('Rotate', 'finished')])
										])

		with _sm_analyse_crowd_2:
			# x:229 y:43
			OperatableStateMachine.add('Analyse',
										_sm_analyse_1,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})

			# x:234 y:182
			OperatableStateMachine.add('Rotate',
										_sm_rotate_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})


		# x:489 y:56, x:261 y:327
		_sm_waiting_and_turn_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['half_turn'])

		with _sm_waiting_and_turn_3:
			# x:30 y:49
			OperatableStateMachine.add('Wait 10s',
										WaitState(wait_time=10),
										transitions={'done': 'action_turn'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:52
			OperatableStateMachine.add('action_turn',
										self.use_behavior(action_turnSM, 'Waiting And Turn/action_turn'),
										transitions={'finished': 'finished', 'failed': 'Cant turn'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'rotation': 'half_turn'})

			# x:237 y:190
			OperatableStateMachine.add('Cant turn',
										SaraSay(sentence="I can't turn !", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:60 y:76
			OperatableStateMachine.add('WaitForBegining',
										ContinueButton(),
										transitions={'true': 'Start Speech', 'false': 'Start Speech'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:253 y:76
			OperatableStateMachine.add('Start Speech',
										SaraSay(sentence="Hum, I want to play riddles !", emotion=1, block=True),
										transitions={'done': 'Waiting And Turn'},
										autonomy={'done': Autonomy.Off})

			# x:403 y:76
			OperatableStateMachine.add('Waiting And Turn',
										_sm_waiting_and_turn_3,
										transitions={'finished': 'Analyse Crowd', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'half_turn': 'half_turn'})

			# x:648 y:76
			OperatableStateMachine.add('Analyse Crowd',
										_sm_analyse_crowd_2,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
