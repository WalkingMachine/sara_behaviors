#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check2')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.FIFO_Add import FIFO_Add
from sara_flexbe_states.continue_button import ContinueButton
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 12 mai 2018
@author: Véronica Romero
'''
class Scenario_Security_check2SM(Behavior):
    '''
    englobe le scenario du test de securite.
    '''


    def __init__(self):
        super(Scenario_Security_check2SM, self).__init__()
        self.name = 'Scenario_Security_check2'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:905 y:319
        _state_machine = OperatableStateMachine(outcomes=['finished'], input_keys=['MedFIFO'])
        _state_machine.userdata.WaitForStart = ["WaitForContinue"]
        _state_machine.userdata.MoveToTestZone = ["Move","TestZone","",""]
        _state_machine.userdata.MoveToExit = ["Move","Exit","",""]
        _state_machine.userdata.MoveOut = ["Move","Out","",""]
        _state_machine.userdata.MedFIFO = []
        _state_machine.userdata.ContinueButton = []
        _state_machine.userdata.WaitForDoor = ["WaitForDoor"]

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:28 y:26
            OperatableStateMachine.add('wait for start (door open)',
                                        FIFO_Add(),
                                        transitions={'done': 'wait for door'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForStart', 'FIFO': 'MedFIFO'})

            # x:29 y:196
            OperatableStateMachine.add('Move to test zone',
                                        FIFO_Add(),
                                        transitions={'done': 'Wait for continue'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveToTestZone', 'FIFO': 'MedFIFO'})

            # x:207 y:197
            OperatableStateMachine.add('Wait for continue',
                                        FIFO_Add(),
                                        transitions={'done': 'Bouton continuer'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForStart', 'FIFO': 'MedFIFO'})

            # x:594 y:194
            OperatableStateMachine.add('Move to exit',
                                        FIFO_Add(),
                                        transitions={'done': 'Wait For Door'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveToExit', 'FIFO': 'MedFIFO'})

            # x:730 y:304
            OperatableStateMachine.add('get out',
                                        FIFO_Add(),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'MoveOut', 'FIFO': 'MedFIFO'})

            # x:35 y:101
            OperatableStateMachine.add('Bouton to start',
                                        ContinueButton(),
                                        transitions={'true': 'Move to test zone', 'false': 'wait for start (door open)'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

            # x:368 y:194
            OperatableStateMachine.add('Bouton continuer',
                                        ContinueButton(),
                                        transitions={'true': 'Move to exit', 'false': 'Bouton continuer'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

            # x:239 y:75
            OperatableStateMachine.add('wait for door',
                                        FIFO_Add(),
                                        transitions={'done': 'Bouton to start'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForDoor', 'FIFO': 'MedFIFO'})

            # x:595 y:286
            OperatableStateMachine.add('Wait For Door',
                                        FIFO_Add(),
                                        transitions={'done': 'get out'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Entry': 'WaitForDoor', 'FIFO': 'MedFIFO'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
