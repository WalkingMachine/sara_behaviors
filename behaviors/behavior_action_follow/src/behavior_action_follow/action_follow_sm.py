#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_follow')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from sara_flexbe_states.sara_say import SaraSay
from behavior_get_operator.get_operator_sm import Get_operatorSM
from sara_flexbe_states.SetKey import SetKey
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
		self.add_behavior(Get_operatorSM, 'Following/Update person/Get_operator')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:572 y:135
		_state_machine = OperatableStateMachine(outcomes=['failed'], input_keys=['ID', 'distance'])
		_state_machine.userdata.ID = 74
		_state_machine.userdata.distance = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:682 y:270, x:520 y:708
		_sm_update_person_0 = OperatableStateMachine(outcomes=['not_found', 'update'], input_keys=['ID', 'TargetPose', 'distance'], output_keys=['TargetPose'])

		with _sm_update_person_0:
			# x:59 y:96
			OperatableStateMachine.add('wait1',
										WaitState(wait_time=1),
										transitions={'done': 'GetEntityByID'},
										autonomy={'done': Autonomy.Off})

			# x:41 y:412
			OperatableStateMachine.add('getPositionFromEntity',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 'Get_Reacheable_Waypoint'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'position'})

			# x:41 y:709
			OperatableStateMachine.add('Get_Reacheable_Waypoint',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'lo'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'position', 'distance': 'distance', 'pose_out': 'TargetPose'})

			# x:41 y:260
			OperatableStateMachine.add('GetEntityByID',
										GetEntityByID(),
										transitions={'found': 'getPositionFromEntity', 'not_found': 'say lost'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:271 y:703
			OperatableStateMachine.add('lo',
										LogKeyState(text="send {}", severity=Logger.REPORT_HINT),
										transitions={'done': 'update'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'TargetPose'})

			# x:213 y:227
			OperatableStateMachine.add('say lost',
										SaraSay(sentence="Sorry, I lost you.", emotion=1, block=True),
										transitions={'done': 'Get_operator'},
										autonomy={'done': Autonomy.Off})

			# x:369 y:262
			OperatableStateMachine.add('Get_operator',
										self.use_behavior(Get_operatorSM, 'Following/Update person/Get_operator'),
										transitions={'Found': 'getPositionFromEntity', 'NotFound': 'not_found'},
										autonomy={'Found': Autonomy.Inherit, 'NotFound': Autonomy.Inherit},
										remapping={'Operator': 'E'})


		# x:130 y:365
		_sm_move_to_person_1 = OperatableStateMachine(outcomes=['failed'], input_keys=['TargetPose'], output_keys=['TargetPose'])

		with _sm_move_to_person_1:
			# x:124 y:145
			OperatableStateMachine.add('move',
										SaraMoveBase(),
										transitions={'arrived': 'failed', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'TargetPose'})


		# x:599 y:319, x:391 y:169, x:151 y:375, x:37 y:281
		_sm_following_2 = ConcurrencyContainer(outcomes=['not_found', 'updatePose'], input_keys=['ID', 'TargetPose', 'distance'], output_keys=['TargetPose'], conditions=[
										('not_found', [('Update person', 'not_found')]),
										('updatePose', [('Update person', 'update'), ('Move to person', 'failed')])
										])

		with _sm_following_2:
			# x:148 y:153
			OperatableStateMachine.add('Move to person',
										_sm_move_to_person_1,
										transitions={'failed': 'updatePose'},
										autonomy={'failed': Autonomy.Inherit},
										remapping={'TargetPose': 'TargetPose'})

			# x:545 y:150
			OperatableStateMachine.add('Update person',
										_sm_update_person_0,
										transitions={'not_found': 'not_found', 'update': 'updatePose'},
										autonomy={'not_found': Autonomy.Inherit, 'update': Autonomy.Inherit},
										remapping={'ID': 'ID', 'TargetPose': 'TargetPose', 'distance': 'distance'})



		with _state_machine:
			# x:95 y:26
			OperatableStateMachine.add('En',
										GetEntityByID(),
										transitions={'found': 'dist', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Entity'})

			# x:300 y:408
			OperatableStateMachine.add('log',
										LogKeyState(text="{}", severity=Logger.REPORT_HINT),
										transitions={'done': 'Following'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'TargetPose'})

			# x:77 y:212
			OperatableStateMachine.add('pos',
										CalculationState(calculation=lambda x: x.position),
										transitions={'done': 're'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'Entity', 'output_value': 'TargetPose'})

			# x:287 y:299
			OperatableStateMachine.add('Following',
										_sm_following_2,
										transitions={'not_found': 'failed', 'updatePose': 'log'},
										autonomy={'not_found': Autonomy.Inherit, 'updatePose': Autonomy.Inherit},
										remapping={'ID': 'ID', 'TargetPose': 'TargetPose', 'distance': 'distance'})

			# x:47 y:307
			OperatableStateMachine.add('re',
										Get_Reacheable_Waypoint(),
										transitions={'done': 'Following'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose_in': 'TargetPose', 'distance': 'distance', 'pose_out': 'TargetPose'})

			# x:90 y:113
			OperatableStateMachine.add('dist',
										SetKey(Value=1),
										transitions={'done': 'pos'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'distance'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
