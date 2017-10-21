#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_pick')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_action_get_entity_pose.action_get_entity_pose_sm import Action_get_entity_poseSM
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.move_arm_pose import MoveArmPose
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
from behavior_check_reachability.check_reachability_sm import Check_reachabilitySM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Oct 20 2017
@author: Philippe La Madeleine
'''
class Action_pickSM(Behavior):
    '''
    Try to pick an object
    '''


    def __init__(self):
        super(Action_pickSM, self).__init__()
        self.name = 'Action_pick'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_get_entity_poseSM, 'get_pose_1')
        self.add_behavior(Action_get_entity_poseSM, 'get_pose_2')
        self.add_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose')
        self.add_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose_2')
        self.add_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose_3')
        self.add_behavior(Check_reachabilitySM, 'Check_reachability')
        self.add_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose')
        self.add_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose_2')
        self.add_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose_3')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:597 y:593, x:287 y:320, x:275 y:449, x:292 y:221, x:450 y:146
        _state_machine = OperatableStateMachine(outcomes=['success', 'too far', 'unreachable', 'not seen', 'critical fail'], input_keys=['object'], output_keys=['grip_pose'])
        _state_machine.userdata.object = ""
        _state_machine.userdata.grip_pose = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:795 y:320, x:816 y:488
        _sm_container_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['object'], output_keys=['pose'])

        with _sm_container_0:
            # x:30 y:40
            OperatableStateMachine.add('Action_get_entity_pose',
                                        self.use_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose'),
                                        transitions={'found': 'gen1', 'not found': 'gen1'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:296 y:282
            OperatableStateMachine.add('gen2',
                                        GenGripperPose(x=0, y=0, z=0, t=0.5),
                                        transitions={'done': 'move2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:297 y:441
            OperatableStateMachine.add('gen3',
                                        GenGripperPose(x=0, y=0, z=0, t=-0.5),
                                        transitions={'done': 'move3'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:519 y:135
            OperatableStateMachine.add('move1',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'Action_get_entity_pose_2'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:524 y:306
            OperatableStateMachine.add('move2',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'Action_get_entity_pose_3'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:528 y:462
            OperatableStateMachine.add('move3',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:27 y:209
            OperatableStateMachine.add('Action_get_entity_pose_2',
                                        self.use_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose_2'),
                                        transitions={'found': 'gen2', 'not found': 'gen2'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:35 y:381
            OperatableStateMachine.add('Action_get_entity_pose_3',
                                        self.use_behavior(Action_get_entity_poseSM, 'Container/Action_get_entity_pose_3'),
                                        transitions={'found': 'gen3', 'not found': 'gen3'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:293 y:116
            OperatableStateMachine.add('gen1',
                                        GenGripperPose(x=0, y=0, z=0, t=0),
                                        transitions={'done': 'move1'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})


        # x:855 y:303, x:856 y:566
        _sm_approach_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['object'])

        with _sm_approach_1:
            # x:39 y:60
            OperatableStateMachine.add('Action_get_entity_pose',
                                        self.use_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose'),
                                        transitions={'found': 'gen1', 'not found': 'gen1'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:331 y:112
            OperatableStateMachine.add('gen1',
                                        GenGripperPose(x=-0.1, y=0, z=0, t=0),
                                        transitions={'done': 'move1'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:542 y:197
            OperatableStateMachine.add('move1',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'Action_get_entity_pose_2'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:334 y:294
            OperatableStateMachine.add('gen2',
                                        GenGripperPose(x=-0.1, y=-0.2, z=0, t=0.5),
                                        transitions={'done': 'move2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:543 y:364
            OperatableStateMachine.add('move2',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'Action_get_entity_pose_3'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:333 y:452
            OperatableStateMachine.add('gen3',
                                        GenGripperPose(x=-0.1, y=0.2, z=0, t=-0.5),
                                        transitions={'done': 'move3'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:543 y:494
            OperatableStateMachine.add('move3',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:27 y:240
            OperatableStateMachine.add('Action_get_entity_pose_2',
                                        self.use_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose_2'),
                                        transitions={'found': 'gen2', 'not found': 'gen2'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:31 y:413
            OperatableStateMachine.add('Action_get_entity_pose_3',
                                        self.use_behavior(Action_get_entity_poseSM, 'approach/Action_get_entity_pose_3'),
                                        transitions={'found': 'gen3', 'not found': 'gen3'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})



        with _state_machine:
            # x:44 y:32
            OperatableStateMachine.add('get_pose_1',
                                        self.use_behavior(Action_get_entity_poseSM, 'get_pose_1'),
                                        transitions={'found': 'PreGripPose', 'not found': 'PreGripPose'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:32 y:210
            OperatableStateMachine.add('get_pose_2',
                                        self.use_behavior(Action_get_entity_poseSM, 'get_pose_2'),
                                        transitions={'found': 'Check_reachability', 'not found': 'not seen'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:50 y:388
            OperatableStateMachine.add('approach',
                                        _sm_approach_1,
                                        transitions={'finished': 'Container', 'failed': 'unreachable'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'object': 'object'})

            # x:45 y:132
            OperatableStateMachine.add('PreGripPose',
                                        MoveArmNamedPose(pose_name="PreGripPose", wait=True),
                                        transitions={'done': 'get_pose_2', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:36 y:298
            OperatableStateMachine.add('Check_reachability',
                                        self.use_behavior(Check_reachabilitySM, 'Check_reachability'),
                                        transitions={'ok': 'approach', 'too_far': 'too far'},
                                        autonomy={'ok': Autonomy.Inherit, 'too_far': Autonomy.Inherit},
                                        remapping={'pose': 'pose'})

            # x:53 y:495
            OperatableStateMachine.add('Container',
                                        _sm_container_0,
                                        transitions={'finished': 'gen up', 'failed': 'unreachable'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'object': 'object', 'pose': 'pose'})

            # x:52 y:585
            OperatableStateMachine.add('gen up',
                                        GenGripperPose(x=0, y=0, z=0.1, t=0),
                                        transitions={'done': 'move up'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:231 y:577
            OperatableStateMachine.add('move up',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'move back', 'failed': 'move back'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:398 y:576
            OperatableStateMachine.add('move back',
                                        MoveArmNamedPose(pose_name="PostGripPose", wait=True),
                                        transitions={'done': 'success', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
