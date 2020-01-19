#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_behaviors.action_move_sm import Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.cupboard_door_detector import CupboardDoorDetector
from sara_flexbe_states.SetKey import SetKey
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.run_trajectory import RunTrajectory
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jan 23 2019
@author: Philippe La Madeleine
'''
class Action_OpenCupboardSM(Behavior):
	'''
	Se déplace vers une armoire pour l'ouvrir
	'''


	def __init__(self):
		super(Action_OpenCupboardSM, self).__init__()
		self.name = 'Action_OpenCupboard'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Action_Move')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:732 y:366, x:29 y:248
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['name'])
		_state_machine.userdata.name = "cupboard"

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:781 y:57, x:292 y:451
		_sm_openit_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_openit_0:
			# x:252 y:38
			OperatableStateMachine.add('init tryal',
										SetKey(Value=3),
										transitions={'done': 'movearm'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'try'})

			# x:451 y:168
			OperatableStateMachine.add('isOpened',
										CupboardDoorDetector(timeout=30),
										transitions={'open': 'yay', 'closed': 'subtryal'},
										autonomy={'open': Autonomy.Off, 'closed': Autonomy.Off})

			# x:464 y:305
			OperatableStateMachine.add('subtryal',
										CalculationState(calculation=lambda x: x-1),
										transitions={'done': 'is ok'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'try', 'output_value': 'try'})

			# x:47 y:300
			OperatableStateMachine.add('is ok',
										CheckConditionState(predicate=lambda x: x>0),
										transitions={'true': 'saytryagain', 'false': 'say cant'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'try'})

			# x:53 y:179
			OperatableStateMachine.add('saytryagain',
										SaraSay(sentence="Let's try again!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'movearm'},
										autonomy={'done': Autonomy.Off})

			# x:44 y:438
			OperatableStateMachine.add('say cant',
										SaraSay(sentence="I can't open it.", input_keys=[], emotion=2, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:455 y:40
			OperatableStateMachine.add('yay',
										SaraSay(sentence="Yay, I did it!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:247 y:175
			OperatableStateMachine.add('movearm',
										RunTrajectory(file="OuvrePorte3", duration=0),
										transitions={'done': 'isOpened'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:310 y:31
			OperatableStateMachine.add('Action_Move',
										self.use_behavior(Action_MoveSM, 'Action_Move'),
										transitions={'finished': 'reach', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'name'})

			# x:326 y:351
			OperatableStateMachine.add('sayWillOpen',
										SaraSay(sentence="The door is closed. I will open it.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'OpenIt'},
										autonomy={'done': Autonomy.Off})

			# x:320 y:229
			OperatableStateMachine.add('checkdoor',
										CupboardDoorDetector(timeout=5),
										transitions={'open': 'finished', 'closed': 'sayWillOpen'},
										autonomy={'open': Autonomy.Off, 'closed': Autonomy.Off})

			# x:338 y:126
			OperatableStateMachine.add('reach',
										SaraSay(sentence="I reached the cupboard!", input_keys=[], emotion=1, block=True),
										transitions={'done': 'checkdoor'},
										autonomy={'done': Autonomy.Off})

			# x:320 y:485
			OperatableStateMachine.add('OpenIt',
										_sm_openit_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
