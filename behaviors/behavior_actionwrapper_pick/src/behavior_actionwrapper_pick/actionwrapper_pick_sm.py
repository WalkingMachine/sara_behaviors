#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from behavior_action_pick.action_pick_sm import Action_pickSM
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.list_entities_by_name import list_entities_by_name
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_PickSM(Behavior):
	'''
	action wrapper pour pick
	'''


	def __init__(self):
		super(ActionWrapper_PickSM, self).__init__()
		self.name = 'ActionWrapper_Pick'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_pickSM, 'Action_pick')
		self.add_behavior(action_look_at_faceSM, 'action_look_at_face')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 506 16 
		# Pick|n1- object



	def create(self):
		# x:573 y:362, x:584 y:226, x:715 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action', 'ObjectInGripper'])
		_state_machine.userdata.Action = ["Pick","cup",""]
		_state_machine.userdata.ObjectInGripper = False
		_state_machine.userdata.room = 1
		_state_machine.userdata.id = None
		_state_machine.userdata.color = None
		_state_machine.userdata.type = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:330 y:124, x:272 y:201
		_sm_get_object_0 = OperatableStateMachine(outcomes=['not_found', 'done'], input_keys=['Action'], output_keys=['ObjectName', 'ID', 'Object'])

		with _sm_get_object_0:
			# x:39 y:40
			OperatableStateMachine.add('get object name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'get objects'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'ObjectName'})

			# x:30 y:114
			OperatableStateMachine.add('get objects',
										list_entities_by_name(frontality_level=0.5),
										transitions={'found': 'GetObject', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'name': 'ObjectName', 'entity_list': 'Objects', 'number': 'number'})

			# x:36 y:274
			OperatableStateMachine.add('get closest ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Object', 'output_value': 'ID'})

			# x:42 y:193
			OperatableStateMachine.add('GetObject',
										CalculationState(calculation=lambda x: x[0]),
										transitions={'done': 'get closest ID'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Objects', 'output_value': 'Object'})



		with _state_machine:
			# x:42 y:31
			OperatableStateMachine.add('check if gripper full',
										GetRosParam(ParamName="behavior/Gripper_Content"),
										transitions={'done': 'say full', 'failed': 'cond'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ObjectInGripper'})

			# x:41 y:112
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] == ''),
										transitions={'true': 'not told', 'false': 'object given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:233 y:110
			OperatableStateMachine.add('not told',
										SaraSay(sentence="Hum! They didn't told me what to pick", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:348 y:487
			OperatableStateMachine.add('got it',
										SaraSayKey(Format=lambda x: "I have the "+x, emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectName'})

			# x:224 y:34
			OperatableStateMachine.add('say full',
										SaraSayKey(Format=lambda x: "Wait. There is already a "+ x + "in my gripper.", emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectInGripper'})

			# x:23 y:478
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'got it', 'unreachable': 'failed', 'not found': 'say lost', 'dropped': 'failed'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'ID'})

			# x:261 y:249
			OperatableStateMachine.add('say lost',
										SaraSayKey(Format=lambda x: "Hum! I lost sight of the "++x, emotion=1, block=True),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectName'})

			# x:47 y:182
			OperatableStateMachine.add('object given',
										SaraSayKey(Format=lambda x: "I'm going to pick that "+x[1], emotion=1, block=True),
										transitions={'done': 'Get object'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:37 y:258
			OperatableStateMachine.add('Get object',
										_sm_get_object_0,
										transitions={'not_found': 'say lost', 'done': 'action_look_at_face'},
										autonomy={'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'ObjectName': 'ObjectName', 'ID': 'ID', 'Object': 'Object'})

			# x:14 y:363
			OperatableStateMachine.add('action_look_at_face',
										self.use_behavior(action_look_at_faceSM, 'action_look_at_face'),
										transitions={'finished': 'Action_pick', 'failed': 'Action_pick'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'Object'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
