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
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.move_arm_named_pose import MoveArmNamedPose
from behavior_check_reachability.check_reachability_sm import Check_reachabilitySM
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.for_loop import ForLoop
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
        self.add_behavior(Action_get_entity_poseSM, 'get_pose')
        self.add_behavior(Check_reachabilitySM, 'Check_reachability')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:885 y:552, x:437 y:201, x:511 y:522, x:587 y:39, x:552 y:394, x:881 y:285
        _state_machine = OperatableStateMachine(outcomes=['success', 'too far', 'unreachable', 'not seen', 'critical fail', 'missed'], input_keys=['object'], output_keys=['grip_pose'])
        _state_machine.userdata.object = "bottle"
        _state_machine.userdata.grip_pose = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:795 y:320, x:293 y:566
        _sm_get_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'], output_keys=['pose'])

        with _sm_get_0:
            # x:293 y:116
            OperatableStateMachine.add('gen1',
                                        GenGripperPose(x=0.04, y=0, z=0, t=0),
                                        transitions={'done': 'move1'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:297 y:441
            OperatableStateMachine.add('gen3',
                                        GenGripperPose(x=0.04, y=0, z=0, t=-0.5),
                                        transitions={'done': 'move3'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:519 y:135
            OperatableStateMachine.add('move1',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'gen2'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:524 y:306
            OperatableStateMachine.add('move2',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'gen3'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:528 y:462
            OperatableStateMachine.add('move3',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:296 y:282
            OperatableStateMachine.add('gen2',
                                        GenGripperPose(x=0.04, y=0, z=0, t=0.5),
                                        transitions={'done': 'move2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})


        # x:855 y:303, x:334 y:582
        _sm_approach_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose'], output_keys=['pose'])

        with _sm_approach_1:
            # x:301 y:83
            OperatableStateMachine.add('gen1',
                                        GenGripperPose(x=-0.1, y=0, z=0, t=0),
                                        transitions={'done': 'say1'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:542 y:197
            OperatableStateMachine.add('move1',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'say2'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:334 y:294
            OperatableStateMachine.add('gen2',
                                        GenGripperPose(x=-0.1, y=-0.1, z=0, t=0.5),
                                        transitions={'done': 'move2'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:543 y:364
            OperatableStateMachine.add('move2',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'say3'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:333 y:452
            OperatableStateMachine.add('gen3',
                                        GenGripperPose(x=-0.1, y=0.1, z=0, t=-0.5),
                                        transitions={'done': 'move3'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:543 y:494
            OperatableStateMachine.add('move3',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'finished', 'failed': 'say4'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:464 y:120
            OperatableStateMachine.add('say1',
                                        SaraSay(sentence="I will try to take it", emotion=1, block=False),
                                        transitions={'done': 'move1'},
                                        autonomy={'done': Autonomy.Off})

            # x:161 y:204
            OperatableStateMachine.add('say2',
                                        SaraSay(sentence="This is hard for me. Just wait a bit longer.", emotion=1, block=False),
                                        transitions={'done': 'gen2'},
                                        autonomy={'done': Autonomy.Off})

            # x:158 y:381
            OperatableStateMachine.add('say3',
                                        SaraSay(sentence="Almost there", emotion=1, block=False),
                                        transitions={'done': 'gen3'},
                                        autonomy={'done': Autonomy.Off})

            # x:448 y:554
            OperatableStateMachine.add('say4',
                                        SaraSay(sentence="Well, I didn't make it. Sorry.", emotion=1, block=False),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:39 y:26
            OperatableStateMachine.add('get_pose',
                                        self.use_behavior(Action_get_entity_poseSM, 'get_pose'),
                                        transitions={'found': 'see it', 'not found': 'say not seen'},
                                        autonomy={'found': Autonomy.Inherit, 'not found': Autonomy.Inherit},
                                        remapping={'name': 'object', 'pose': 'pose'})

            # x:48 y:466
            OperatableStateMachine.add('approach',
                                        _sm_approach_1,
                                        transitions={'finished': 'Get', 'failed': 'back'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose'})

            # x:47 y:392
            OperatableStateMachine.add('PreGripPose',
                                        MoveArmNamedPose(pose_name="PreGripPose", wait=True),
                                        transitions={'done': 'approach', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:44 y:200
            OperatableStateMachine.add('Check_reachability',
                                        self.use_behavior(Check_reachabilitySM, 'Check_reachability'),
                                        transitions={'ok': 'open gripper', 'too_far': 'too far'},
                                        autonomy={'ok': Autonomy.Inherit, 'too_far': Autonomy.Inherit},
                                        remapping={'pose': 'pose'})

            # x:44 y:557
            OperatableStateMachine.add('Get',
                                        _sm_get_0,
                                        transitions={'finished': 'gen up', 'failed': 'back2'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose'})

            # x:45 y:654
            OperatableStateMachine.add('gen up',
                                        GenGripperPose(x=0, y=0, z=0.05, t=0),
                                        transitions={'done': 'close'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pose', 'pose_out': 'pose_out'})

            # x:563 y:653
            OperatableStateMachine.add('move up',
                                        MoveArmPose(wait=True),
                                        transitions={'done': 'move back', 'failed': 'move back'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose_out'})

            # x:736 y:652
            OperatableStateMachine.add('move back',
                                        MoveArmNamedPose(pose_name="PostGripPose", wait=True),
                                        transitions={'done': 'success', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:228 y:642
            OperatableStateMachine.add('close',
                                        SetGripperState(width=0, effort=0.00001),
                                        transitions={'object': 'got it', 'no_object': 'say fail 2'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:56 y:286
            OperatableStateMachine.add('open gripper',
                                        SetGripperState(width=0.14, effort=0),
                                        transitions={'object': 'PreGripPose', 'no_object': 'PreGripPose'},
                                        autonomy={'object': Autonomy.Off, 'no_object': Autonomy.Off},
                                        remapping={'object_size': 'object_size'})

            # x:223 y:451
            OperatableStateMachine.add('back',
                                        MoveArmNamedPose(pose_name="PreGripPose", wait=False),
                                        transitions={'done': 'unreachable', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:220 y:509
            OperatableStateMachine.add('back2',
                                        MoveArmNamedPose(pose_name="PreGripPose", wait=False),
                                        transitions={'done': 'unreachable', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:376 y:573
            OperatableStateMachine.add('back3',
                                        MoveArmNamedPose(pose_name="PreGripPose", wait=False),
                                        transitions={'done': 'missed', 'failed': 'critical fail'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:72 y:118
            OperatableStateMachine.add('see it',
                                        SaraSay(sentence="I see it", emotion=1, block=False),
                                        transitions={'done': 'Check_reachability'},
                                        autonomy={'done': Autonomy.Off})

            # x:273 y:201
            OperatableStateMachine.add('too far',
                                        SaraSay(sentence="But it is too far", emotion=1, block=True),
                                        transitions={'done': 'too_far'},
                                        autonomy={'done': Autonomy.Off})

            # x:375 y:34
            OperatableStateMachine.add('say not seen',
                                        SaraSayKey(Format=lambda x: "I can't see the "+x, emotion=1, block=True),
                                        transitions={'done': 'not seen'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'object'})

            # x:246 y:572
            OperatableStateMachine.add('say fail 2',
                                        SaraSay(sentence="Oops, I missed it.", emotion=1, block=False),
                                        transitions={'done': 'back3'},
                                        autonomy={'done': Autonomy.Off})

            # x:604 y:96
            OperatableStateMachine.add('for',
                                        ForLoop(repeat=1),
                                        transitions={'do': 'again', 'end': 'missed'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})

            # x:376 y:91
            OperatableStateMachine.add('again',
                                        SaraSay(sentence="Let me try again.", emotion=1, block=False),
                                        transitions={'done': 'get_pose'},
                                        autonomy={'done': Autonomy.Off})

            # x:409 y:645
            OperatableStateMachine.add('got it',
                                        SaraSay(sentence="I got it", emotion=1, block=False),
                                        transitions={'done': 'move up'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
