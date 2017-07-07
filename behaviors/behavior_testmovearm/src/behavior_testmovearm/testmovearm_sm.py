#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_testmovearm')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.pose_gen import GenPose
from sara_flexbe_states.FIFO_New import FIFO_New
from sara_flexbe_states.FIFO_Add import FIFO_Add
from behavior_actionmovearm.actionmovearm_sm import ActionMoveArmSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jul 06 2017
@author: Philippe La Madeleine
'''
class TestMoveArmSM(Behavior):
    '''
    test the ActionMoveArm behavior.
    '''


    def __init__(self):
        super(TestMoveArmSM, self).__init__()
        self.name = 'TestMoveArm'

        # parameters of this behavior
        self.add_parameter('actionName', 'MoveArm')

        # references to used behaviors
        self.add_behavior(ActionMoveArmSM, 'ActionMoveArm')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:872 y:482, x:395 y:220
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.actionName = "MoveArm"

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:22 y:466
            OperatableStateMachine.add('generate pose',
                                        GenPose(),
                                        transitions={'done': 'new action form', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:193 y:467
            OperatableStateMachine.add('new action form',
                                        FIFO_New(),
                                        transitions={'done': 'add action name'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'FIFO': 'ActionForm'})

            # x:352 y:464
            OperatableStateMachine.add('add action name',
                                        FIFO_Add(),
                                        transitions={'done': 'add pose'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'actionName', 'FIFO': 'ActionForm'})

            # x:524 y:471
            OperatableStateMachine.add('add pose',
                                        FIFO_Add(),
                                        transitions={'done': 'ActionMoveArm'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'pose', 'FIFO': 'ActionForm'})

            # x:647 y:460
            OperatableStateMachine.add('ActionMoveArm',
                                        self.use_behavior(ActionMoveArmSM, 'ActionMoveArm'),
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'ActionForm': 'ActionForm'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
