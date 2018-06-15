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
from behavior_action_find.action_find_sm import Action_findSM
from flexbe_states.calculation_state import CalculationState
from behavior_action_look_at_face.action_look_at_face_sm import action_look_at_faceSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
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
		self.add_behavior(Action_findSM, 'find object/Action_find')
		self.add_behavior(action_look_at_faceSM, 'action_look_at_face')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 797 34 
		# Pick|n1- object



	def create(self):
		# x:629 y:497, x:880 y:203, x:715 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Pick","bottle"]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_group_0 = ConcurrencyContainer(outcomes=['done'], input_keys=['pose_out'], conditions=[
										('done', [('move', 'arrived')]),
										('done', [('move', 'failed')]),
										('done', [('3', 'done')])
										])

		with _sm_group_0:
			# x:30 y:40
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'done', 'failed': 'done'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_out'})

			# x:179 y:91
			OperatableStateMachine.add('3',
										WaitState(wait_time=2),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:458, x:130 y:458, x:230 y:458
		_sm_get_object_1 = OperatableStateMachine(outcomes=['failed', 'found', 'not_found'], output_keys=['ID', 'Object'])

		with _sm_get_object_1:
			# x:35 y:40
			OperatableStateMachine.add('get param',
										GetRosParam(ParamName="/behavior/FoundEntity/Id"),
										transitions={'done': 'get obj', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:207 y:223
			OperatableStateMachine.add('get obj',
										GetEntityByID(),
										transitions={'found': 'found', 'not_found': 'not_found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Object'})


		# x:40 y:700
		_sm_get_closer_2 = OperatableStateMachine(outcomes=['done'], input_keys=['Object'])

		with _sm_get_closer_2:
			# x:59 y:36
			OperatableStateMachine.add('set targetpose',
										SetKey(Value="PreGripPose"),
										transitions={'done': 'say closer'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:39 y:367
			OperatableStateMachine.add('set dist',
										SetKey(Value=0.7),
										transitions={'done': 'get close pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:13 y:461
			OperatableStateMachine.add('get close pos',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Group'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'Pos', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:31 y:201
			OperatableStateMachine.add('get pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'move head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Object', 'output_value': 'Pos'})

			# x:26 y:287
			OperatableStateMachine.add('move head',
										SaraSetHeadAngle(pitch=0.7, yaw=0),
										transitions={'done': 'set dist'},
										autonomy={'done': Autonomy.Off})

			# x:189 y:143
			OperatableStateMachine.add('move arm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'get pos', 'failed': 'get pos'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:209 y:36
			OperatableStateMachine.add('say closer',
										SaraSay(sentence="I need to get a bit closer.", emotion=1, block=False),
										transitions={'done': 'move arm'},
										autonomy={'done': Autonomy.Off})

			# x:26 y:541
			OperatableStateMachine.add('Group',
										_sm_group_0,
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'pose_out': 'pose_out'})

			# x:33 y:625
			OperatableStateMachine.add('wait',
										WaitState(wait_time=2),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off})


		# x:421 y:110, x:272 y:201
		_sm_find_object_3 = OperatableStateMachine(outcomes=['not_found', 'done'], input_keys=['Action', 'ObjectName'], output_keys=['ID', 'Object'])

		with _sm_find_object_3:
			# x:27 y:148
			OperatableStateMachine.add('Action_find',
										self.use_behavior(Action_findSM, 'find object/Action_find'),
										transitions={'done': 'get closest ID', 'failed': 'not_found'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'ObjectName', 'entity': 'Object'})

			# x:36 y:274
			OperatableStateMachine.add('get closest ID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'done'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Object', 'output_value': 'ID'})


		# x:59 y:308, x:387 y:59, x:384 y:139
		_sm_check_form_4 = OperatableStateMachine(outcomes=['done', 'fail_full', 'full_no_object'], input_keys=['Action'])

		with _sm_check_form_4:
			# x:31 y:40
			OperatableStateMachine.add('check if gripper full',
										GetRosParam(ParamName="behavior/Gripper_Content"),
										transitions={'done': 'say full', 'failed': 'cond'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ObjectInGripper'})

			# x:30 y:121
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] == ''),
										transitions={'true': 'not told', 'false': 'done'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:222 y:119
			OperatableStateMachine.add('not told',
										SaraSay(sentence="Hum! They didn't told me what to pick", emotion=1, block=True),
										transitions={'done': 'full_no_object'},
										autonomy={'done': Autonomy.Off})

			# x:213 y:43
			OperatableStateMachine.add('say full',
										SaraSayKey(Format=lambda x: "Wait. There is already a "+ x + "in my gripper.", emotion=1, block=True),
										transitions={'done': 'fail_full'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectInGripper'})



		with _state_machine:
			# x:84 y:30
			OperatableStateMachine.add('Check Form',
										_sm_check_form_4,
										transitions={'done': 'get name', 'fail_full': 'cause1', 'full_no_object': 'cause2'},
										autonomy={'done': Autonomy.Inherit, 'fail_full': Autonomy.Inherit, 'full_no_object': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:31 y:493
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(Action_pickSM, 'Action_pick'),
										transitions={'success': 'got it', 'unreachable': 'for 1', 'not found': 'say lost', 'dropped': 'say missed'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'ID'})

			# x:271 y:440
			OperatableStateMachine.add('say lost',
										SaraSayKey(Format=lambda x: "Hum! I lost sight of the "+x, emotion=1, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectName'})

			# x:257 y:144
			OperatableStateMachine.add('find object',
										_sm_find_object_3,
										transitions={'not_found': 'cause3', 'done': 'action_look_at_face'},
										autonomy={'not_found': Autonomy.Inherit, 'done': Autonomy.Inherit},
										remapping={'Action': 'Action', 'ObjectName': 'ObjectName', 'ID': 'ID', 'Object': 'Object'})

			# x:25 y:389
			OperatableStateMachine.add('action_look_at_face',
										self.use_behavior(action_look_at_faceSM, 'action_look_at_face'),
										transitions={'finished': 'Action_pick', 'failed': 'Action_pick'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Entity': 'Object'})

			# x:261 y:239
			OperatableStateMachine.add('Get closer',
										_sm_get_closer_2,
										transitions={'done': 'find object'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Object': 'Object'})

			# x:275 y:333
			OperatableStateMachine.add('for 1',
										ForLoop(repeat=1),
										transitions={'do': 'Get closer', 'end': 'say giveup'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:364 y:318
			OperatableStateMachine.add('say giveup',
										SaraSay(sentence="I give up", emotion=1, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off})

			# x:271 y:388
			OperatableStateMachine.add('say missed',
										SaraSay(sentence="Oops! I missed.", emotion=1, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off})

			# x:273 y:487
			OperatableStateMachine.add('got it',
										SaraSayKey(Format=lambda x: "I have the "+x, emotion=1, block=True),
										transitions={'done': 'set param'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'ObjectName'})

			# x:443 y:497
			OperatableStateMachine.add('set param',
										SetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ObjectName'})

			# x:40 y:128
			OperatableStateMachine.add('get name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Get object'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'ObjectName'})

			# x:29 y:261
			OperatableStateMachine.add('Get object',
										_sm_get_object_1,
										transitions={'failed': 'find object', 'found': 'action_look_at_face', 'not_found': 'find object'},
										autonomy={'failed': Autonomy.Inherit, 'found': Autonomy.Inherit, 'not_found': Autonomy.Inherit},
										remapping={'ID': 'ID', 'Object': 'Object'})

			# x:511 y:20
			OperatableStateMachine.add('cause1',
										SetKey(Value="My gripper was already full."),
										transitions={'done': 'setrosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:512 y:81
			OperatableStateMachine.add('cause2',
										SetKey(Value="I didn't know what to pick."),
										transitions={'done': 'setrosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:511 y:143
			OperatableStateMachine.add('cause3',
										SetKey(Value="I didn't found the object."),
										transitions={'done': 'setrosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:690 y:197
			OperatableStateMachine.add('setrosparam',
										SetRosParam(ParamName="behavior/GPSR/CauseOfFailure"),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'Key'})

			# x:527 y:315
			OperatableStateMachine.add('cause4',
										SetKey(Value="I was unable to pick the object."),
										transitions={'done': 'setrosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
