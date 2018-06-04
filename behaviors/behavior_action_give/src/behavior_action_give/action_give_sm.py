#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_give')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.SetRosParam import SetRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
from flexbe_states.calculation_state import CalculationState
from sara_flexbe_states.get_reachable_waypoint import Get_Reacheable_Waypoint
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.torque_reader import ReadTorque
from sara_flexbe_states.sara_say import SaraSay
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 10 2018
@author: Philippe La Madeleine
'''
class Action_GiveSM(Behavior):
    '''
    give the content of the gripper to a person.
    '''


    def __init__(self):
        super(Action_GiveSM, self).__init__()
        self.name = 'Action_Give'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_MoveSM, 'give/Follow/Action_Move')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
		
		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1195 y:433, x:135 y:397, x:1125 y:546
        _state_machine = OperatableStateMachine(outcomes=['Given', 'Person_not_found', 'fail'], input_keys=['person_id'])
        _state_machine.userdata.person_id = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

        # x:299 y:300, x:263 y:535
        _sm_give_0 = OperatableStateMachine(outcomes=['failed', 'given'], input_keys=['Object'])

        with _sm_give_0:
            # x:67 y:27
            OperatableStateMachine.add('SetPose',
                                        SetKey(Value="ShowGripper"),
                                        transitions={'done': 'moveArm'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'target'})

            # x:53 y:413
            OperatableStateMachine.add('read torque',
                                        ReadTorque(watchdog=5, Joint="right_elbow_pitch_joint", Threshold=2, min_time=1),
                                        transitions={'threshold': 'open gripper', 'watchdog': 'read torque', 'fail': 'failed'},
                                        autonomy={'threshold': Autonomy.Off, 'watchdog': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'torque': 'torque'})

            # x:52 y:500
            OperatableStateMachine.add('open gripper',
                                        SetGripperState(width=0.15, effort=1),
                                        transitions={'object': 'given', 'no_object': 'given'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:64 y:248
            OperatableStateMachine.add('say pull',
                                        SaraSay(sentence="You can pull on it", emotion=1, block=False),
                                        transitions={'done': 'wait 1'},
                                        autonomy={'done': Autonomy.Off})

            # x:64 y:325
            OperatableStateMachine.add('wait 1',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'read torque'},
                                        autonomy={'done': Autonomy.Off})

            # x:57 y:175
            OperatableStateMachine.add('moveArm',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'say pull', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'target'})


        # x:326 y:455, x:291 y:228
        _sm_follow_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ID'])

        with _sm_follow_1:
            # x:39 y:30
            OperatableStateMachine.add('not rel',
                                        SetKey(Value=False),
                                        transitions={'done': 'set dist'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'relative'})

            # x:43 y:279
            OperatableStateMachine.add('get person',
                                        GetEntityByID(),
                                        transitions={'found': 'get pos', 'not_found': 'get person'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
                                        remapping={'ID': 'ID', 'Entity': 'Entity'})

            # x:60 y:372
            OperatableStateMachine.add('get pos',
                                        CalculationState(calculation=lambda x: x.position),
                                        transitions={'done': 'reac'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'Entity', 'output_value': 'pose_in'})

            # x:56 y:458
            OperatableStateMachine.add('reac',
                                        Get_Reacheable_Waypoint(),
                                        transitions={'done': 'Action_Move'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose_in', 'distance': 'distance', 'pose_out': 'pose_out'})

            # x:30 y:115
            OperatableStateMachine.add('set dist',
                                        SetKey(Value=1),
                                        transitions={'done': 'get person'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'distance'})

            # x:254 y:329
            OperatableStateMachine.add('Action_Move',
                                        self.use_behavior(Action_MoveSM, 'give/Follow/Action_Move'),
                                        transitions={'finished': 'get person', 'failed': 'Action_Move'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose_out', 'relative': 'relative'})


        # x:313 y:247, x:301 y:177, x:103 y:293, x:303 y:113, x:88 y:385, x:311 y:57, x:93 y:335, x:304 y:15
        _sm_give_2 = ConcurrencyContainer(outcomes=['failed', 'given', 'continue', 'person_lost'], input_keys=['ID'], conditions=[
                                        ('failed', [('Give', 'failed')]),
                                        ('given', [('Give', 'given')]),
                                        ('given', [('Follow', 'finished')]),
                                        ('failed', [('Follow', 'failed')])
                                        ])

        with _sm_give_2:
            # x:91 y:50
            OperatableStateMachine.add('Follow',
                                        _sm_follow_1,
                                        transitions={'finished': 'given', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'ID': 'ID'})

            # x:84 y:164
            OperatableStateMachine.add('Give',
                                        _sm_give_0,
                                        transitions={'failed': 'failed', 'given': 'given'},
                                        autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit},
                                        remapping={'Object': 'Object'})



        with _state_machine:
            # x:288 y:222
            OperatableStateMachine.add('give',
                                        _sm_give_2,
                                        transitions={'failed': 'log movebase fail', 'given': 'set idle pose', 'continue': 'give', 'person_lost': 'Person_not_found'},
                                        autonomy={'failed': Autonomy.Inherit, 'given': Autonomy.Inherit, 'continue': Autonomy.Inherit, 'person_lost': Autonomy.Inherit},
                                        remapping={'ID': 'person_id'})

            # x:815 y:527
            OperatableStateMachine.add('log movebase fail',
                                        LogState(text="giving Failed", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'fail'},
                                        autonomy={'done': Autonomy.Off})

            # x:863 y:76
            OperatableStateMachine.add('set idle pose',
                                        SetKey(Value="IdlePose"),
                                        transitions={'done': 'moveArm2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'target'})

            # x:1174 y:94
            OperatableStateMachine.add('moveArm2',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'set none', 'failed': 'log moveitfail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'target'})

            # x:1167 y:337
            OperatableStateMachine.add('close gripper',
                                        SetGripperState(width=0, effort=1),
                                        transitions={'object': 'Given', 'no_object': 'Given'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:1258 y:255
            OperatableStateMachine.add('remove gripper content',
                                        SetRosParam(ParamName="GripperContent"),
                                        transitions={'done': 'close gripper'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Value': 'none'})

            # x:1180 y:179
            OperatableStateMachine.add('set none',
                                        SetKey(Value=None),
                                        transitions={'done': 'close gripper'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'none'})

            # x:971 y:298
            OperatableStateMachine.add('log moveitfail',
                                        LogState(text="moveit failed", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'fail'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
