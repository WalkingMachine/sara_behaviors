#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_move_base import SaraMoveBase
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 25 2017
@author: Philippe La Madeleine
'''
class Scenario_Security_checkSM(Behavior):
    '''
    englobe le scénario du test de sécurité.
- On attend l'ouverture d'une porte
- avance jusqu’à un waypoint spécifique
- attend quelques secondes
- vas au waypoint de sortie
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

        # O 297 41 
        # - On attend l'ouverture d'une porte|n- avance jusqu’à un waypoint spécifique|n- attend quelques secondes|n- vas au waypoint de sortie



    def create(self):
        # x:864 y:228, x:848 y:452
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.waypoint = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:30 y:308
        _sm_door_management_0 = OperatableStateMachine(outcomes=['done'])

        with _sm_door_management_0:
            # x:30 y:40
            OperatableStateMachine.add('detect door',
                                        DoorDetector(timeout=5),
                                        transitions={'done': 'done', 'failed': 'call for door opening'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:187 y:136
            OperatableStateMachine.add('call for door opening',
                                        SaraSay(sentence="I can't open a door by myself. Could you open that door for me please?", emotion=1),
                                        transitions={'done': 'detect door again'},
                                        autonomy={'done': Autonomy.Off})

            # x:588 y:209
            OperatableStateMachine.add('say thank you',
                                        SaraSay(sentence="Thank you!", emotion=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})

            # x:395 y:181
            OperatableStateMachine.add('detect door again',
                                        DoorDetector(timeout=10),
                                        transitions={'done': 'say thank you', 'failed': 'call for door again'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:190 y:239
            OperatableStateMachine.add('call for door again',
                                        SaraSay(sentence="Can someone open this door for me please", emotion=1),
                                        transitions={'done': 'detect door again'},
                                        autonomy={'done': Autonomy.Off})



        with _state_machine:
            # x:65 y:54
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'Door management'},
                                        autonomy={'done': Autonomy.Off})

            # x:46 y:192
            OperatableStateMachine.add('Door management',
                                        _sm_door_management_0,
                                        transitions={'done': 'move the robot'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:648 y:207
            OperatableStateMachine.add('move the robot',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'finished', 'failed': 'error'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'waypoint': 'waypoint'})

            # x:300 y:431
            OperatableStateMachine.add('Sorry no waypoint',
                                        SaraSay(sentence="Sorry, I don't know where to go.", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})

            # x:664 y:348
            OperatableStateMachine.add('error',
                                        SaraSay(sentence="Sorry, I seem to have trouble with my navigation system", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
