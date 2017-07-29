#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_action_executor')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.FIFO_Get import FIFO_Get
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.decision_state import DecisionState
from behavior_actionwrapper_bring.actionwrapper_bring_sm import ActionWrapper_BringSM
from behavior_actionwrapper_follow.actionwrapper_follow_sm import ActionWrapper_FollowSM
from behavior_actionwrapper_move.actionwrapper_move_sm import ActionWrapper_MoveSM
from behavior_actionwrapper_attach.actionwrapper_attach_sm import ActionWrapper_AttachSM
from behavior_actionwrapper_lookat.actionwrapper_lookat_sm import ActionWrapper_LookAtSM
from behavior_actionwrapper_find.actionwrapper_find_sm import ActionWrapper_FindSM
from behavior_actionwrapper_place.actionwrapper_place_sm import ActionWrapper_PlaceSM
from behavior_actionwrapper_give.actionwrapper_give_sm import ActionWrapper_GiveSM
from behavior_actionwrapper_pick.actionwrapper_pick_sm import ActionWrapper_PickSM
from behavior_actionwrapper_turn.actionwrapper_turn_sm import ActionWrapper_TurnSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 25 2017
@author: Philippe La Madeleine
'''
class SaraactionexecutorSM(Behavior):
    '''
    Execute les actions liste par le command interpretor
    '''


    def __init__(self):
        super(SaraactionexecutorSM, self).__init__()
        self.name = 'Sara action executor'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(ActionWrapper_BringSM, 'Action/ActionWrapper_Bring')
        self.add_behavior(ActionWrapper_FollowSM, 'Action/ActionWrapper_Follow')
        self.add_behavior(ActionWrapper_MoveSM, 'Action/ActionWrapper_Move')
        self.add_behavior(ActionWrapper_AttachSM, 'Action/ActionWrapper_Attach')
        self.add_behavior(ActionWrapper_LookAtSM, 'Action/ActionWrapper_LookAt')
        self.add_behavior(ActionWrapper_FindSM, 'Action/ActionWrapper_Find')
        self.add_behavior(ActionWrapper_PlaceSM, 'Action/ActionWrapper_Place')
        self.add_behavior(ActionWrapper_GiveSM, 'Action/ActionWrapper_Give')
        self.add_behavior(ActionWrapper_PickSM, 'Action/ActionWrapper_Pick')
        self.add_behavior(ActionWrapper_TurnSM, 'Action/ActionWrapper_Turn')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:835 y:96, x:834 y:255
        _state_machine = OperatableStateMachine(outcomes=['CriticalFail', 'Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO'])
        _state_machine.userdata.HighFIFO = []
        _state_machine.userdata.MedFIFO = [['Move','forward']]
        _state_machine.userdata.LowFIFO = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:896 y:331, x:913 y:610, x:913 y:7
        _sm_action_0 = OperatableStateMachine(outcomes=['Shutdown', 'CriticalFail', 'done'], input_keys=['Action'])

        with _sm_action_0:
            # x:53 y:27
            OperatableStateMachine.add('log1',
                                        LogKeyState(text="{}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'ActionIdentification'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'Action'})

            # x:8 y:264
            OperatableStateMachine.add('ActionIdentification',
                                        DecisionState(outcomes=['Bring', 'Follow', 'Move', 'Attach', 'LookAt', 'Find', 'Place', 'Give', 'Pick', 'Turn'], conditions=lambda x: x[0]),
                                        transitions={'Bring': 'ActionWrapper_Bring', 'Follow': 'ActionWrapper_Follow', 'Move': 'ActionWrapper_Move', 'Attach': 'ActionWrapper_Attach', 'LookAt': 'ActionWrapper_LookAt', 'Find': 'ActionWrapper_Find', 'Place': 'ActionWrapper_Place', 'Give': 'ActionWrapper_Give', 'Pick': 'ActionWrapper_Pick', 'Turn': 'ActionWrapper_Turn'},
                                        autonomy={'Bring': Autonomy.Off, 'Follow': Autonomy.Off, 'Move': Autonomy.Off, 'Attach': Autonomy.Off, 'LookAt': Autonomy.Off, 'Find': Autonomy.Off, 'Place': Autonomy.Off, 'Give': Autonomy.Off, 'Pick': Autonomy.Off, 'Turn': Autonomy.Off},
                                        remapping={'input_value': 'Action'})

            # x:413 y:27
            OperatableStateMachine.add('ActionWrapper_Bring',
                                        self.use_behavior(ActionWrapper_BringSM, 'Action/ActionWrapper_Bring'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:411 y:86
            OperatableStateMachine.add('ActionWrapper_Follow',
                                        self.use_behavior(ActionWrapper_FollowSM, 'Action/ActionWrapper_Follow'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:411 y:144
            OperatableStateMachine.add('ActionWrapper_Move',
                                        self.use_behavior(ActionWrapper_MoveSM, 'Action/ActionWrapper_Move'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:409 y:202
            OperatableStateMachine.add('ActionWrapper_Attach',
                                        self.use_behavior(ActionWrapper_AttachSM, 'Action/ActionWrapper_Attach'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:408 y:261
            OperatableStateMachine.add('ActionWrapper_LookAt',
                                        self.use_behavior(ActionWrapper_LookAtSM, 'Action/ActionWrapper_LookAt'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:416 y:320
            OperatableStateMachine.add('ActionWrapper_Find',
                                        self.use_behavior(ActionWrapper_FindSM, 'Action/ActionWrapper_Find'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:414 y:378
            OperatableStateMachine.add('ActionWrapper_Place',
                                        self.use_behavior(ActionWrapper_PlaceSM, 'Action/ActionWrapper_Place'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:418 y:437
            OperatableStateMachine.add('ActionWrapper_Give',
                                        self.use_behavior(ActionWrapper_GiveSM, 'Action/ActionWrapper_Give'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:420 y:496
            OperatableStateMachine.add('ActionWrapper_Pick',
                                        self.use_behavior(ActionWrapper_PickSM, 'Action/ActionWrapper_Pick'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:420 y:558
            OperatableStateMachine.add('ActionWrapper_Turn',
                                        self.use_behavior(ActionWrapper_TurnSM, 'Action/ActionWrapper_Turn'),
                                        transitions={'finished': 'done', 'failed': 'CriticalFail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})



        with _state_machine:
            # x:104 y:46
            OperatableStateMachine.add('wait for 0.1 s',
                                        WaitState(wait_time=0.1),
                                        transitions={'done': 'Get HighAction'},
                                        autonomy={'done': Autonomy.Off})

            # x:298 y:262
            OperatableStateMachine.add('Get MedAction',
                                        FIFO_Get(),
                                        transitions={'done': 'Action', 'empty': 'Get LowAction'},
                                        autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off},
                                        remapping={'FIFO': 'MedFIFO', 'Out': 'Action'})

            # x:301 y:377
            OperatableStateMachine.add('Get LowAction',
                                        FIFO_Get(),
                                        transitions={'done': 'Action', 'empty': 'wait for 0.1 s'},
                                        autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off},
                                        remapping={'FIFO': 'LowFIFO', 'Out': 'Action'})

            # x:584 y:146
            OperatableStateMachine.add('Action',
                                        _sm_action_0,
                                        transitions={'Shutdown': 'Shutdown', 'CriticalFail': 'CriticalFail', 'done': 'wait for 0.1 s'},
                                        autonomy={'Shutdown': Autonomy.Inherit, 'CriticalFail': Autonomy.Inherit, 'done': Autonomy.Inherit},
                                        remapping={'Action': 'Action'})

            # x:294 y:154
            OperatableStateMachine.add('Get HighAction',
                                        FIFO_Get(),
                                        transitions={'done': 'Action', 'empty': 'Get MedAction'},
                                        autonomy={'done': Autonomy.Off, 'empty': Autonomy.Off},
                                        remapping={'FIFO': 'HighFIFO', 'Out': 'Action'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
