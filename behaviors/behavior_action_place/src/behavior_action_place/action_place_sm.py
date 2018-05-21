#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_place')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.TF_transform import TF_transformation
from sara_flexbe_states.gen_gripper_pose import GenGripperPose
from sara_flexbe_states.moveit_move import MoveitMove
from sara_flexbe_states.SetKey import SetKey
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Raphael Duchaine
'''
class Action_placeSM(Behavior):
    '''
    Place un objet a une position
    '''


    def __init__(self):
        super(Action_placeSM, self).__init__()
        self.name = 'Action_place'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:

        # O 47 132 
        # TF Transform |nFrame1 Frame2|n

        # O 806 75 
        # Gen Grip pose|n|nA

        # O 185 36 
        # MoveIt move|nmove = false|n|nPos

        # O 365 42 
        # PreGrip Pose #pre grip

        # O 532 14 
        # #approach_pos|nGen Grip pose|ndistance = 0.25

        # O 826 172 
        # MoveIt move|nmove =True|n|nA

        # O 730 314 
        # open grip

        # O 651 33 
        # MoveIt move|nmove =True|n|nB

        # O 650 399 
        # MoveIt move|n|nB

        # O 516 441 
        # #preGrip|nMoveIt move



    def create(self):
        # x:221 y:414, x:530 y:205
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pos'])
        _state_machine.userdata.pos = 0

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:102 y:240
            OperatableStateMachine.add('TF_transformation',
                                        TF_transformation(in_ref="map", out_ref="base_link"),
                                        transitions={'done': 'MoveIt_isReachable', 'fail': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'fail': Autonomy.Off},
                                        remapping={'in_pos': 'pos', 'out_pos': 'pos'})

            # x:681 y:193
            OperatableStateMachine.add('Gen place_pos',
                                        GenGripperPose(l=0.0),
                                        transitions={'done': 'setOpened'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pos', 'pose_out': 'grip_pose'})

            # x:681 y:106
            OperatableStateMachine.add('Move_approach',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'Gen place_pos', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'approach_pose'})

            # x:348 y:82
            OperatableStateMachine.add('gotoPreGrip',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'Gen approach_pos', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'PreGripPose'})

            # x:172 y:117
            OperatableStateMachine.add('MoveIt_isReachable',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'setPreGripPose', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'pos'})

            # x:260 y:196
            OperatableStateMachine.add('setPreGripPose',
                                        SetKey(Value="PreGripPose"),
                                        transitions={'done': 'gotoPreGrip'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'PreGripPose'})

            # x:652 y:257
            OperatableStateMachine.add('Open_grip',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'ReturnApproachPose', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'Opened'})

            # x:827 y:246
            OperatableStateMachine.add('setOpened',
                                        SetKey(Value="Opened"),
                                        transitions={'done': 'Open_grip'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'Opened'})

            # x:485 y:85
            OperatableStateMachine.add('Gen approach_pos',
                                        GenGripperPose(l=0.25),
                                        transitions={'done': 'Move_approach'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose_in': 'pos', 'pose_out': 'approach_pose'})

            # x:512 y:315
            OperatableStateMachine.add('ReturnApproachPose',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'ReturnPreGrip', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'approach_pose'})

            # x:326 y:337
            OperatableStateMachine.add('ReturnPreGrip',
                                        MoveitMove(move=True, waitForExecution=True, group="RightArm"),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'target': 'PreGripPose'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
