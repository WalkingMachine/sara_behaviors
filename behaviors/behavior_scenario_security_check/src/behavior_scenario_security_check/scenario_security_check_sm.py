#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.FIFO_Add import FIFO_Add
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe La Madeleine
'''
class Scenario_Security_checkSM(Behavior):
    '''
    englobe le scenario du test de securite.
    '''


    def __init__(self):
        super(Scenario_Security_checkSM, self).__init__()
        self.name = 'Scenario_Security_check'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:696 y:158
        _state_machine = OperatableStateMachine(outcomes=['finished'], input_keys=['MedFIFO'])
        _state_machine.userdata.WaitForStart = ["WaitForContinue"]
        _state_machine.userdata.WaitForDoor = ["WaitForDoor"]
        _state_machine.userdata.MoveToTestZone = ["Move","TestZone","",""]
        _state_machine.userdata.MoveToExit = ["Move","Exit","",""]
        _state_machine.userdata.MoveOut = ["Move","Out","",""]
        _state_machine.userdata.MedFIFO = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:79 y:87
            OperatableStateMachine.add('wait for start',
                                        FIFO_Add(),
                                        transitions={'done': 'wait for door'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForStart', 'FIFO': 'MedFIFO'})

            # x:80 y:186
            OperatableStateMachine.add('wait for door',
                                        FIFO_Add(),
                                        transitions={'done': 'Move to test zone'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForDoor', 'FIFO': 'MedFIFO'})

            # x:90 y:277
            OperatableStateMachine.add('Move to test zone',
                                        FIFO_Add(),
                                        transitions={'done': 'Wait for continue'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveToTestZone', 'FIFO': 'MedFIFO'})

            # x:244 y:364
            OperatableStateMachine.add('Wait for continue',
                                        FIFO_Add(),
                                        transitions={'done': 'Move to exit'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForStart', 'FIFO': 'MedFIFO'})

            # x:463 y:355
            OperatableStateMachine.add('Move to exit',
                                        FIFO_Add(),
                                        transitions={'done': 'WaitFor door'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveToExit', 'FIFO': 'MedFIFO'})

            # x:603 y:357
            OperatableStateMachine.add('WaitFor door',
                                        FIFO_Add(),
                                        transitions={'done': 'get out'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForDoor', 'FIFO': 'MedFIFO'})

            # x:672 y:243
            OperatableStateMachine.add('get out',
                                        FIFO_Add(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveOut', 'FIFO': 'MedFIFO'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
