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
        # x:772 y:365, x:745 y:232
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:65 y:54
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'detect door'},
                                        autonomy={'done': Autonomy.Off})

            # x:81 y:180
            OperatableStateMachine.add('detect door',
                                        DoorDetector(timeout=5),
                                        transitions={'done': 'finished', 'failed': 'call for door opening'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:96 y:314
            OperatableStateMachine.add('call for door opening',
                                        SaraSay(sentence="Could you open that door please", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
