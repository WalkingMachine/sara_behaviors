#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_follow import SaraFollow
from sara_flexbe_states.KeepLookingAt import KeepLookingAt
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Apr 30 2018
@author: Raphael Duchaine
'''
class Action_followSM(Behavior):
	'''
	Permet de suivre quelqu'un.
Demande le id de la personne a suivre
	'''


	def __init__(self):
		super(Action_followSM, self).__init__()
		self.name = 'Action_follow'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:572 y:135
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 2

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:365
		_sm_delai_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_delai_0:
			# x:129 y:168
			OperatableStateMachine.add('delay',
										WaitState(wait_time=25),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_turn_head_1 = OperatableStateMachine(outcomes=['fail'])

		with _sm_turn_head_1:
			# x:75 y:47
			OperatableStateMachine.add('turn r',
										SaraSetHeadAngle(pitch=0, yaw=-1.5),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:673 y:293
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=8),
										transitions={'done': 'turn right'},
										autonomy={'done': Autonomy.Off})

			# x:369 y:464
			OperatableStateMachine.add('turn right',
										SaraSetHeadAngle(pitch=0, yaw=-1.5),
										transitions={'done': 'wait2'},
										autonomy={'done': Autonomy.Off})

			# x:165 y:362
			OperatableStateMachine.add('wait2',
										WaitState(wait_time=8),
										transitions={'done': 'turn left'},
										autonomy={'done': Autonomy.Off})

			# x:240 y:48
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'turn left'},
										autonomy={'done': Autonomy.Off})

			# x:429 y:68
			OperatableStateMachine.add('turn left',
										SaraSetHeadAngle(pitch=0, yaw=1.5),
										transitions={'done': 'wait1'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_search_2 = OperatableStateMachine(outcomes=['found'], input_keys=['ID'])

		with _sm_search_2:
			# x:91 y:163
			OperatableStateMachine.add('get en',
										GetEntityByID(),
										transitions={'found': 'found', 'not_found': 'get en'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})


		# x:30 y:365, x:530 y:244, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_find_back_3 = ConcurrencyContainer(outcomes=['back', 'not_found'], input_keys=['ID'], conditions=[
										('back', [('search', 'found')]),
										('back', [('Turn head', 'fail')]),
										('not_found', [('Delai', 'finished')])
										])

		with _sm_find_back_3:
			# x:145 y:108
			OperatableStateMachine.add('search',
										_sm_search_2,
										transitions={'found': 'back'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:469 y:136
			OperatableStateMachine.add('Turn head',
										_sm_turn_head_1,
										transitions={'fail': 'back'},
										autonomy={'fail': Autonomy.Inherit})

			# x:281 y:192
			OperatableStateMachine.add('Delai',
										_sm_delai_0,
										transitions={'finished': 'not_found'},
										autonomy={'finished': Autonomy.Inherit})


		# x:30 y:458
		_sm_look_at_4 = OperatableStateMachine(outcomes=['fail'], input_keys=['ID'])

		with _sm_look_at_4:
			# x:231 y:115
			OperatableStateMachine.add('look',
										KeepLookingAt(),
										transitions={'failed': 'sorry'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})

			# x:470 y:272
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Sorry, I lost you. Please wait for me! Make sure to let me see your face, please.", emotion=1, block=False),
										transitions={'done': 'Find back'},
										autonomy={'done': Autonomy.Off})

			# x:103 y:276
			OperatableStateMachine.add('Found you',
										SaraSay(sentence="Here you are!", emotion=1, block=False),
										transitions={'done': 'look'},
										autonomy={'done': Autonomy.Off})

			# x:248 y:264
			OperatableStateMachine.add('Find back',
										_sm_find_back_3,
										transitions={'back': 'Found you', 'not_found': 'fail'},
										autonomy={'back': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		# x:30 y:365
		_sm_follow_5 = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])

		with _sm_follow_5:
			# x:65 y:167
			OperatableStateMachine.add('follow',
										SaraFollow(distance=1.2),
										transitions={'failed': 'follow'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:368 y:271, x:423 y:158, x:230 y:458
		_sm_follow_6 = ConcurrencyContainer(outcomes=['not_found'], input_keys=['ID'], conditions=[
										('not_found', [('Look at', 'fail')]),
										('not_found', [('Follow', 'failed')])
										])

		with _sm_follow_6:
			# x:185 y:134
			OperatableStateMachine.add('Follow',
										_sm_follow_5,
										transitions={'failed': 'not_found'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:123 y:236
			OperatableStateMachine.add('Look at',
										_sm_look_at_4,
										transitions={'fail': 'not_found'},
										autonomy={'fail': Autonomy.Inherit},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:150 y:130
			OperatableStateMachine.add('Follow',
										_sm_follow_6,
										transitions={'not_found': 'failed'},
										autonomy={'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
