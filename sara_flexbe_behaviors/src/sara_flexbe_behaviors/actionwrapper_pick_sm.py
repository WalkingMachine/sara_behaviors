#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.GetRosParam import GetRosParam
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_behaviors.action_pick_sm import Action_pickSM as sara_flexbe_behaviors__Action_pickSM
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_set_head_angle import SaraSetHeadAngle
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_behaviors.action_find_sm import Action_findSM as sara_flexbe_behaviors__Action_findSM
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
		self.add_behavior(sara_flexbe_behaviors__Action_pickSM, 'Action_pick')
		self.add_behavior(sara_flexbe_behaviors__Action_findSM, 'Action_find')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 797 34 
		# Pick|n1- object



	def create(self):
		# x:660 y:509, x:880 y:203, x:715 y:440
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


		# x:40 y:700
		_sm_get_closer_1 = OperatableStateMachine(outcomes=['done'], input_keys=['Object'])

		with _sm_get_closer_1:
			# x:59 y:36
			OperatableStateMachine.add('set targetpose',
										SetKey(Value="PreGripPose"),
										transitions={'done': 'say closer'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'target'})

			# x:88 y:374
			OperatableStateMachine.add('set dist',
										SetKey(Value=0.8),
										transitions={'done': 'get close pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})

			# x:26 y:448
			OperatableStateMachine.add('get close pos',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Group'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'Pos', 'distance': 'distance', 'pose_out': 'pose_out'})

			# x:47 y:213
			OperatableStateMachine.add('get pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'move head'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Object', 'output_value': 'Pos'})

			# x:88 y:290
			OperatableStateMachine.add('move head',
										SaraSetHeadAngle(pitch=0.7, yaw=0),
										transitions={'done': 'set dist'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:156
			OperatableStateMachine.add('move arm',
										MoveitMove(move=True, waitForExecution=True, group="RightArm"),
										transitions={'done': 'get pos', 'failed': 'get pos'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target': 'target'})

			# x:60 y:106
			OperatableStateMachine.add('say closer',
										SaraSay(sentence="I need to get a bit closer.", input_keys=[], emotion=1, block=False),
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


		# x:59 y:308, x:447 y:59, x:384 y:162
		_sm_check_form_2 = OperatableStateMachine(outcomes=['done', 'fail_full', 'full_no_object'], input_keys=['Action'])

		with _sm_check_form_2:
			# x:31 y:40
			OperatableStateMachine.add('check if gripper full',
										GetRosParam(ParamName="behavior/Gripper_Content"),
										transitions={'done': 'Say_Full', 'failed': 'cond'},
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
										SaraSay(sentence="Hum! They didn't told me what to pick", input_keys=[], emotion=1, block=True),
										transitions={'done': 'full_no_object'},
										autonomy={'done': Autonomy.Off})

			# x:242 y:31
			OperatableStateMachine.add('Say_Full',
										SaraSay(sentence=lambda x: "Wait. There is already a "+ x + "in my gripper.", input_keys=[], emotion=0, block=True),
										transitions={'done': 'fail_full'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:84 y:30
			OperatableStateMachine.add('Check Form',
										_sm_check_form_2,
										transitions={'done': 'get name', 'fail_full': 'cause1', 'full_no_object': 'cause2'},
										autonomy={'done': Autonomy.Inherit, 'fail_full': Autonomy.Inherit, 'full_no_object': Autonomy.Inherit},
										remapping={'Action': 'Action'})

			# x:28 y:452
			OperatableStateMachine.add('Action_pick',
										self.use_behavior(sara_flexbe_behaviors__Action_pickSM, 'Action_pick'),
										transitions={'success': 'Got_It', 'unreachable': 'for 1', 'not found': 'Say_lost', 'dropped': 'say missed'},
										autonomy={'success': Autonomy.Inherit, 'unreachable': Autonomy.Inherit, 'not found': Autonomy.Inherit, 'dropped': Autonomy.Inherit},
										remapping={'objectID': 'ID'})

			# x:261 y:239
			OperatableStateMachine.add('Get closer',
										_sm_get_closer_1,
										transitions={'done': 'Action_find'},
										autonomy={'done': Autonomy.Inherit},
										remapping={'Object': 'Object'})

			# x:275 y:333
			OperatableStateMachine.add('for 1',
										ForLoop(repeat=1),
										transitions={'do': 'Get closer', 'end': 'say giveup'},
										autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
										remapping={'index': 'index'})

			# x:416 y:264
			OperatableStateMachine.add('say giveup',
										SaraSay(sentence="I give up", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off})

			# x:284 y:496
			OperatableStateMachine.add('say missed',
										SaraSay(sentence="Oops! I missed.", input_keys=[], emotion=1, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off})

			# x:469 y:495
			OperatableStateMachine.add('set param',
										SetRosParam(ParamName="behavior/GripperContent"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'Value': 'ObjectName'})

			# x:82 y:115
			OperatableStateMachine.add('get name',
										CalculationState(calculation=lambda x: x[1]),
										transitions={'done': 'Action_find'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Action', 'output_value': 'ObjectName'})

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

			# x:605 y:312
			OperatableStateMachine.add('cause4',
										SetKey(Value="I was unable to pick the object."),
										transitions={'done': 'setrosparam'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'Key'})

			# x:30 y:188
			OperatableStateMachine.add('Action_find',
										self.use_behavior(sara_flexbe_behaviors__Action_findSM, 'Action_find'),
										transitions={'done': 'getID', 'failed': 'cause3'},
										autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'className': 'ObjectName', 'entity': 'Object'})

			# x:49 y:322
			OperatableStateMachine.add('getID',
										CalculationState(calculation=lambda x: x.ID),
										transitions={'done': 'Action_pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Object', 'output_value': 'ID'})

			# x:284 y:422
			OperatableStateMachine.add('Say_lost',
										SaraSay(sentence=lambda x: "Hum! I lost sight of the "+x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'cause4'},
										autonomy={'done': Autonomy.Off})

			# x:281 y:572
			OperatableStateMachine.add('Got_It',
										SaraSay(sentence=lambda x: "I have the "+x, input_keys=[], emotion=0, block=True),
										transitions={'done': 'set param'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
