#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_executor')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.decision_state import DecisionState
from behavior_actionwrapper_ask.actionwrapper_ask_sm import ActionWrapper_AskSM
from behavior_actionwrapper_bring.actionwrapper_bring_sm import ActionWrapper_BringSM
from behavior_actionwrapper_count.actionwrapper_count_sm import ActionWrapper_CountSM
from behavior_actionwrapper_find.actionwrapper_find_sm import ActionWrapper_FindSM
from behavior_actionwrapper_find_person.actionwrapper_find_person_sm import ActionWrapper_Find_PersonSM
from behavior_actionwrapper_follow.actionwrapper_follow_sm import ActionWrapper_FollowSM
from behavior_actionwrapper_give.actionwrapper_give_sm import ActionWrapper_GiveSM
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
from behavior_actionwrapper_place.actionwrapper_place_sm import ActionWrapper_PlaceSM
from behavior_actionwrapper_say.actionwrapper_say_sm import ActionWrapper_SaySM
from behavior_actionwrapper_answer.actionwrapper_answer_sm import ActionWrapper_AnswerSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 30 2018
@author: Philippe La Madeleine
'''
class Action_ExecutorSM(Behavior):
	'''
	Execute une action a partir d'un ActionForm.
	'''


	def __init__(self):
		super(Action_ExecutorSM, self).__init__()
		self.name = 'Action_Executor'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(ActionWrapper_AskSM, 'ActionWrapper_Ask')
		self.add_behavior(ActionWrapper_BringSM, 'ActionWrapper_Bring')
		self.add_behavior(ActionWrapper_CountSM, 'ActionWrapper_Count')
		self.add_behavior(ActionWrapper_FindSM, 'ActionWrapper_Find')
		self.add_behavior(ActionWrapper_Find_PersonSM, 'ActionWrapper_Find_Person')
		self.add_behavior(ActionWrapper_FollowSM, 'ActionWrapper_Follow')
		self.add_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give')
		self.add_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move')
		self.add_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick')
		self.add_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place')
		self.add_behavior(ActionWrapper_SaySM, 'ActionWrapper_Say')
		self.add_behavior(ActionWrapper_AnswerSM, 'ActionWrapper_Answer')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:887 y:426, x:1209 y:79, x:1066 y:156
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Move", "GPSR"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:50 y:28
			OperatableStateMachine.add('decide Action',
										DecisionState(outcomes=["Answer", "Ask", "Bring", "Count", "Find", "FindPerson", "Follow", "Give", "Move", "Pick", "Place", "Say"], conditions=lambda x: x[0]),
										transitions={'Answer': 'ActionWrapper_Answer', 'Ask': 'ActionWrapper_Ask', 'Bring': 'ActionWrapper_Bring', 'Count': 'ActionWrapper_Count', 'Find': 'ActionWrapper_Find', 'FindPerson': 'ActionWrapper_Find_Person', 'Follow': 'ActionWrapper_Follow', 'Give': 'ActionWrapper_Give', 'Move': 'ActionWrapper_Move', 'Pick': 'ActionWrapper_Pick', 'Place': 'ActionWrapper_Place', 'Say': 'ActionWrapper_Say'},
										autonomy={'Answer': Autonomy.Off, 'Ask': Autonomy.Off, 'Bring': Autonomy.Off, 'Count': Autonomy.Off, 'Find': Autonomy.Off, 'FindPerson': Autonomy.Off, 'Follow': Autonomy.Off, 'Give': Autonomy.Off, 'Move': Autonomy.Off, 'Pick': Autonomy.Off, 'Place': Autonomy.Off, 'Say': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:479 y:59
			OperatableStateMachine.add('ActionWrapper_Ask',
										self.use_behavior(ActionWrapper_AskSM, 'ActionWrapper_Ask'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:471 y:118
			OperatableStateMachine.add('ActionWrapper_Bring',
										self.use_behavior(ActionWrapper_BringSM, 'ActionWrapper_Bring'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:466 y:177
			OperatableStateMachine.add('ActionWrapper_Count',
										self.use_behavior(ActionWrapper_CountSM, 'ActionWrapper_Count'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})

			# x:471 y:294
			OperatableStateMachine.add('ActionWrapper_Find',
										self.use_behavior(ActionWrapper_FindSM, 'ActionWrapper_Find'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:435 y:235
			OperatableStateMachine.add('ActionWrapper_Find_Person',
										self.use_behavior(ActionWrapper_Find_PersonSM, 'ActionWrapper_Find_Person'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:461 y:352
			OperatableStateMachine.add('ActionWrapper_Follow',
										self.use_behavior(ActionWrapper_FollowSM, 'ActionWrapper_Follow'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:468 y:410
			OperatableStateMachine.add('ActionWrapper_Give',
										self.use_behavior(ActionWrapper_GiveSM, 'ActionWrapper_Give'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:463 y:468
			OperatableStateMachine.add('ActionWrapper_Move',
										self.use_behavior(ActionWrapper_MoveSM, 'ActionWrapper_Move'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:468 y:526
			OperatableStateMachine.add('ActionWrapper_Pick',
										self.use_behavior(ActionWrapper_PickSM, 'ActionWrapper_Pick'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action', 'ObjectInGripper': 'Action'})

			# x:463 y:584
			OperatableStateMachine.add('ActionWrapper_Place',
										self.use_behavior(ActionWrapper_PlaceSM, 'ActionWrapper_Place'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:470 y:642
			OperatableStateMachine.add('ActionWrapper_Say',
										self.use_behavior(ActionWrapper_SaySM, 'ActionWrapper_Say'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:464 y:1
			OperatableStateMachine.add('ActionWrapper_Answer',
										self.use_behavior(ActionWrapper_AnswerSM, 'ActionWrapper_Answer'),
										transitions={'finished': 'finished', 'failed': 'failed', 'critical_fail': 'critical_fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'critical_fail': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
