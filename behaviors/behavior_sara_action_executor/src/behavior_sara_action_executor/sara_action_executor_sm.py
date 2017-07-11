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
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 25 2017
@author: Philippe La Madeleine
'''
class SaraactionexecutorSM(Behavior):
    '''
    Execute les actions listé par le command interpretor
    '''


    def __init__(self):
        super(SaraactionexecutorSM, self).__init__()
        self.name = 'Sara action executor'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:835 y:96, x:834 y:255
        _state_machine = OperatableStateMachine(outcomes=['CriticalFail', 'Shutdown'], input_keys=['HighFIFO', 'MedFIFO', 'LowFIFO'])
        _state_machine.userdata.HighFIFO = [""]
        _state_machine.userdata.MedFIFO = [""]
        _state_machine.userdata.LowFIFO = ["shutdown"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:857 y:155, x:863 y:450, x:869 y:295
        _sm_action_0 = OperatableStateMachine(outcomes=['Shutdown', 'CriticalFail', 'done'], input_keys=['Action'])

        with _sm_action_0:
            # x:44 y:119
            OperatableStateMachine.add('log1',
                                        LogKeyState(text="{}", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'ActionIdentification'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'data': 'Action'})

            # x:30 y:252
            OperatableStateMachine.add('ActionIdentification',
                                        DecisionState(outcomes=['Bring', 'Follow', 'MoveBase', 'Attach', 'LookAt', 'Find', 'Place', 'Give', 'Pick', 'Turn'], conditions=lambda x: x[0]),
                                        transitions={'Bring': 'done', 'Follow': 'done', 'MoveBase': 'done', 'Attach': 'done', 'LookAt': 'done', 'Find': 'done', 'Place': 'done', 'Give': 'done', 'Pick': 'done', 'Turn': 'done'},
                                        autonomy={'Bring': Autonomy.Off, 'Follow': Autonomy.Off, 'MoveBase': Autonomy.Off, 'Attach': Autonomy.Off, 'LookAt': Autonomy.Off, 'Find': Autonomy.Off, 'Place': Autonomy.Off, 'Give': Autonomy.Off, 'Pick': Autonomy.Off, 'Turn': Autonomy.Off},
                                        remapping={'input_value': 'Action'})



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
