#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

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
		# x:272 y:55
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 4

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:470 y:563
		_sm_delai_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_delai_0:
			# x:167 y:26
			OperatableStateMachine.add('say lost',
										SaraSay(sentence="Sorry, I lost you.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'delay'},
										autonomy={'done': Autonomy.Off})

			# x:167 y:190
			OperatableStateMachine.add('say wait',
										SaraSay(sentence=" Please wait for me!", input_keys=[], emotion=0, block=False),
										transitions={'done': 'delay2'},
										autonomy={'done': Autonomy.Off})

			# x:161 y:362
			OperatableStateMachine.add('say face 2',
										SaraSay(sentence="Make sure to let me see your face, please.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'delay3'},
										autonomy={'done': Autonomy.Off})

			# x:173 y:278
			OperatableStateMachine.add('delay2',
										WaitState(wait_time=3),
										transitions={'done': 'say face 2'},
										autonomy={'done': Autonomy.Off})

			# x:169 y:448
			OperatableStateMachine.add('delay3',
										WaitState(wait_time=4),
										transitions={'done': 'say get closer'},
										autonomy={'done': Autonomy.Off})

			# x:176 y:108
			OperatableStateMachine.add('delay',
										WaitState(wait_time=3),
										transitions={'done': 'say wait'},
										autonomy={'done': Autonomy.Off})

			# x:142 y:547
			OperatableStateMachine.add('say get closer',
										SaraSay(sentence="I need you to get closer please.", input_keys=[], emotion=0, block=False),
										transitions={'done': 'delais4'},
										autonomy={'done': Autonomy.Off})

			# x:315 y:543
			OperatableStateMachine.add('delais4',
										WaitState(wait_time=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_turn_head_1 = OperatableStateMachine(outcomes=['fail'])

		with _sm_turn_head_1:
			# x:54 y:55
			OperatableStateMachine.add('turn r',
										SaraSetHeadAngle(pitch=0, yaw=-1.5),
										transitions={'done': 'w3'},
										autonomy={'done': Autonomy.Off})

			# x:749 y:183
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=5),
										transitions={'done': 'turn right'},
										autonomy={'done': Autonomy.Off})

			# x:727 y:309
			OperatableStateMachine.add('turn right',
										SaraSetHeadAngle(pitch=0, yaw=-1.5),
										transitions={'done': 'wait2'},
										autonomy={'done': Autonomy.Off})

			# x:582 y:311
			OperatableStateMachine.add('wait2',
										WaitState(wait_time=5),
										transitions={'done': 'center2'},
										autonomy={'done': Autonomy.Off})

			# x:246 y:54
			OperatableStateMachine.add('w3',
										WaitState(wait_time=4),
										transitions={'done': 'turn left'},
										autonomy={'done': Autonomy.Off})

			# x:383 y:57
			OperatableStateMachine.add('turn left',
										SaraSetHeadAngle(pitch=0, yaw=1.5),
										transitions={'done': 'wait3'},
										autonomy={'done': Autonomy.Off})

			# x:728 y:69
			OperatableStateMachine.add('center1',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'wait1'},
										autonomy={'done': Autonomy.Off})

			# x:576 y:63
			OperatableStateMachine.add('wait3',
										WaitState(wait_time=5),
										transitions={'done': 'center1'},
										autonomy={'done': Autonomy.Off})

			# x:389 y:308
			OperatableStateMachine.add('center2',
										SaraSetHeadAngle(pitch=0, yaw=0),
										transitions={'done': 'wait4'},
										autonomy={'done': Autonomy.Off})

			# x:409 y:177
			OperatableStateMachine.add('wait4',
										WaitState(wait_time=5),
										transitions={'done': 'turn left'},
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
										transitions={'failed': 'Find back'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})

			# x:78 y:199
			OperatableStateMachine.add('Found you',
										SaraSay(sentence="Here you are!", input_keys=[], emotion=1, block=False),
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
										SaraFollow(distance=1.5, ReplanPeriod=1),
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
			# x:74 y:38
			OperatableStateMachine.add('Follow',
										_sm_follow_6,
										transitions={'not_found': 'failed'},
										autonomy={'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
