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
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
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
		self.add_behavior(action_look_at_faceSM, 'Follow/Look at/action_look_at_face')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:572 y:135
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])
		_state_machine.userdata.ID = 22

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:365
		_sm_turn_head_0 = OperatableStateMachine(outcomes=['fail'])

		with _sm_turn_head_0:
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
		_sm_search_1 = OperatableStateMachine(outcomes=['found'], input_keys=['ID'])

		with _sm_search_1:
			# x:91 y:163
			OperatableStateMachine.add('get en',
										GetEntityByID(),
										transitions={'found': 'found', 'not_found': 'get en'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})


		# x:30 y:365, x:530 y:244, x:230 y:365
		_sm_find_back_2 = ConcurrencyContainer(outcomes=['back'], input_keys=['ID'], conditions=[
										('back', [('search', 'found')]),
										('back', [('Turn head', 'fail')])
										])

		with _sm_find_back_2:
			# x:145 y:108
			OperatableStateMachine.add('search',
										_sm_search_1,
										transitions={'found': 'back'},
										autonomy={'found': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:469 y:136
			OperatableStateMachine.add('Turn head',
										_sm_turn_head_0,
										transitions={'fail': 'back'},
										autonomy={'fail': Autonomy.Inherit})


		# x:30 y:458
		_sm_look_at_3 = OperatableStateMachine(outcomes=['fail'], input_keys=['ID'])

		with _sm_look_at_3:
			# x:110 y:102
			OperatableStateMachine.add('get entity',
										GetEntityByID(),
										transitions={'found': 'action_look_at_face', 'not_found': 'sorry'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})


			# x:422 y:129
			OperatableStateMachine.add('action_look_at_face',
										self.use_behavior(action_look_at_faceSM, 'Follow/Look at/action_look_at_face'),
										transitions={'finished': 'get entity', 'failed': 'sorry'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'Entity'})

			# x:205 y:355
			OperatableStateMachine.add('Find back',
										_sm_find_back_2,
										transitions={'back': 'get entity'},
										autonomy={'back': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:430 y:275
			OperatableStateMachine.add('sorry',
										SaraSay(sentence="Sorry, I lost you. Please wait for me!", emotion=1, block=False),
										transitions={'done': 'Find back'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:365
		_sm_follow_4 = OperatableStateMachine(outcomes=['failed'], input_keys=['ID'])

		with _sm_follow_4:
			# x:65 y:167
			OperatableStateMachine.add('follow',
										SaraFollow(distance=1.2),
										transitions={'failed': 'follow'},
										autonomy={'failed': Autonomy.Off},
										remapping={'ID': 'ID'})


		# x:368 y:271, x:423 y:158, x:230 y:458
		_sm_follow_5 = ConcurrencyContainer(outcomes=['not_found'], input_keys=['ID'], conditions=[
										('not_found', [('Look at', 'fail')]),
										('not_found', [('Follow', 'failed')])
										])

		with _sm_follow_5:
			# x:185 y:134
			OperatableStateMachine.add('Follow',
										_sm_follow_4,
										transitions={'failed': 'not_found'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID'})

			# x:123 y:236
			OperatableStateMachine.add('Look at',
										_sm_look_at_3,
										transitions={'fail': 'not_found'},
										autonomy={'fail': Autonomy.Inherit},
										remapping={'ID': 'ID'})



		with _state_machine:
			# x:150 y:130
			OperatableStateMachine.add('Follow',
										_sm_follow_5,
										transitions={'not_found': 'failed'},
										autonomy={'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
