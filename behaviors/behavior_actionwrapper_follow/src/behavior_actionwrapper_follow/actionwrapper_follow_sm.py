#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_follow.action_follow_sm import Action_followSM
from sara_flexbe_states.get_speech import GetSpeech
from flexbe_states.check_condition_state import CheckConditionState
from behavior_action_lookatfacebase.action_lookatfacebase_sm import action_lookAtFaceBaseSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 22/05/2018
@author: Lucas Maurice
'''
class ActionWrapper_FollowSM(Behavior):
	'''
	action wrapper pour follow
	'''


	def __init__(self):
		super(ActionWrapper_FollowSM, self).__init__()
		self.name = 'ActionWrapper_Follow'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_followSM, 'Follow Loop/Action_follow')
		self.add_behavior(action_lookAtFaceBaseSM, 'action_lookAtFaceBase')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 1262 27 
		# Follow|n1- person|n2- area where the person is|n3- path (unused)

		# O 1260 94 
		# Story|n0- Decompose Command|n1- Find Area|n2- Join Area|n3- Find Person|n4- Follow Person|n5- END

		# O 856 104 
		# - behavior/FoundPerson/Id|n- behavior/FoundPerson/TimeStamp

		# O 351 66 /Follow Loop/Wait Stop
		# Stop|nArrived|nReached|nHere|nOk



	def create(self):
		# x:763 y:423, x:705 y:133, x:896 y:268
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Follow", "rachel"]
		_state_machine.userdata.distance = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:368
		_sm_wait_stop_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_wait_stop_0:
			# x:112 y:116
			OperatableStateMachine.add('Get Command',
										GetSpeech(watchdog=1000),
										transitions={'done': 'Command Stop', 'nothing': 'Get Command', 'fail': 'Get Command'},
										autonomy={'done': Autonomy.Off, 'nothing': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'words': 'words'})

			# x:115 y:270
			OperatableStateMachine.add('Command Stop',
										CheckConditionState(predicate=lambda x: True in [True for match in ['stop', 'arrived', 'reached', 'here', 'ok'] if match in x]),
										transitions={'true': 'finished', 'false': 'Get Command'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'words'})


		# x:395 y:153, x:390 y:47, x:359 y:362, x:304 y:368, x:430 y:368
		_sm_follow_loop_1 = ConcurrencyContainer(outcomes=['finished', 'error'], input_keys=['ID', 'distance'], conditions=[
										('finished', [('Wait Stop', 'finished')]),
										('error', [('Action_follow', 'failed')])
										])

		with _sm_follow_loop_1:
			# x:190 y:37
			OperatableStateMachine.add('Action_follow',
										self.use_behavior(Action_followSM, 'Follow Loop/Action_follow'),
										transitions={'failed': 'error'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'ID': 'ID', 'distance': 'distance'})

			# x:190 y:139
			OperatableStateMachine.add('Wait Stop',
										_sm_wait_stop_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})



		with _state_machine:
			# x:85 y:51
			OperatableStateMachine.add('GetName',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Get Person ID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'name'})

			# x:97 y:141
			OperatableStateMachine.add('Get Person ID',
										GetRosParam(ParamName="/behavior/FoundPerson/Id"),
										transitions={'done': 'Get Entity Location', 'failed': 'Say Lost'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'personId'})

			# x:92 y:225
			OperatableStateMachine.add('Get Entity Location',
										GetEntityByID(),
										transitions={'found': 'Tell Follow', 'not_found': 'Say Lost'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'personId', 'Entity': 'Entity'})

			# x:432 y:129
			OperatableStateMachine.add('Say Lost',
										SaraSayKey(Format=lambda x: "I have lost " + x + " !", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:276 y:424
			OperatableStateMachine.add('Tell Way',
										SaraSay(sentence="Show me the way !", emotion=1, block=True),
										transitions={'done': 'Follow Loop'},
										autonomy={'done': Autonomy.Off})

			# x:97 y:324
			OperatableStateMachine.add('Tell Follow',
										SaraSayKey(Format=lambda x: "I will follow you, " + x + " !", emotion=1, block=True),
										transitions={'done': 'action_lookAtFaceBase'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:385 y:405
			OperatableStateMachine.add('Follow Loop',
										_sm_follow_loop_1,
										transitions={'finished': 'Stop Follow', 'error': 'Cant Follow'},
										autonomy={'finished': Autonomy.Inherit, 'error': Autonomy.Inherit},
										remapping={'ID': 'personId', 'distance': 'distance'})

			# x:416 y:250
			OperatableStateMachine.add('Cant Follow',
										SaraSayKey(Format=lambda x: "I can't follow you, " + x + " !", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:574 y:411
			OperatableStateMachine.add('Stop Follow',
										SaraSayKey(Format=lambda x: "Ok " + x + ", I will stop to follow you !", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'name'})

			# x:53 y:409
			OperatableStateMachine.add('action_lookAtFaceBase',
										self.use_behavior(action_lookAtFaceBaseSM, 'action_lookAtFaceBase'),
										transitions={'finished': 'Tell Way', 'failed': 'Say Lost'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'Entity'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
