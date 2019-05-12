#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.decision_state import DecisionState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.WonderlandGetEntityByID import WonderlandGetEntityByID
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_behaviors.action_place_sm import Action_placeSM
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Apr 29 2019
@author: Raphaël Duchaîne
'''
class clean_upSM(Behavior):
    '''
    Housekeeper scenario Robocup 2019
    '''


    def __init__(self):
        super(clean_upSM, self).__init__()
        self.name = 'clean_up'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_placeSM, 'PutDownObject/Action_place')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
    
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1200 y:570, x:5 y:103
        _state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['___'])
        _state_machine.userdata.___ = ''
        _state_machine.userdata.seenObjects = []
        _state_machine.userdata.containers = []
        _state_machine.userdata.indexNextContainer = 0
        _state_machine.userdata.containerPos = []

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:130 y:465, x:230 y:465
        _sm_saydone_0 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['indexNextContainer'])

        with _sm_saydone_0:
            # x:69 y:26
            OperatableStateMachine.add('Looked all around the house',
                                        SaraSay(sentence="I looked all around the house seeing "+x[0]+" containers", input_keys=['indexNextContainer'], emotion=0, block=True),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'indexNextContainer': 'indexNextContainer'})


        # x:130 y:465
        _sm_continueloop_1 = OperatableStateMachine(outcomes=['done'])

        with _sm_continueloop_1:
            # x:94 y:28
            OperatableStateMachine.add('continue',
                                        WaitState(wait_time=0),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:130 y:465, x:230 y:465
        _sm_complexbehaviorfordeusexmachina_2 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_complexbehaviorfordeusexmachina_2:
            # x:98 y:96
            OperatableStateMachine.add('014',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_askforhelp_3 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_askforhelp_3:
            # x:98 y:96
            OperatableStateMachine.add('013',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465
        _sm_sayyoumissedyourshot_4 = OperatableStateMachine(outcomes=['done'])

        with _sm_sayyoumissedyourshot_4:
            # x:85 y:25
            OperatableStateMachine.add('Oops. Looks like I missed my shot',
                                        SaraSay(sentence="Oops. Looks like I missed my shot", input_keys=[], emotion=0, block=True),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:130 y:465, x:230 y:465
        _sm_putdownobject_5 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['containerPos'])

        with _sm_putdownobject_5:
            # x:91 y:97
            OperatableStateMachine.add('Action_place',
                                        self.use_behavior(Action_placeSM, 'PutDownObject/Action_place'),
                                        transitions={'finished': 'done', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pos': 'containerPos'})


        # x:130 y:465, x:230 y:465
        _sm_gotodesiredcontainer_6 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_gotodesiredcontainer_6:
            # x:105 y:166
            OperatableStateMachine.add('010',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_grabclosestobject_7 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_grabclosestobject_7:
            # x:104 y:38
            OperatableStateMachine.add('Retry 3 times',
                                        ForLoop(repeat=3),
                                        transitions={'do': '09', 'end': 'failed'},
                                        autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
                                        remapping={'index': 'index'})

            # x:36 y:160
            OperatableStateMachine.add('09',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'Retry 3 times'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_scancontainer_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_scancontainer_8:
            # x:98 y:96
            OperatableStateMachine.add('08',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_gotowhilelooking_9 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_gotowhilelooking_9:
            # x:98 y:96
            OperatableStateMachine.add('07',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:120 y:504, x:316 y:455
        _sm_getunseencontainer_10 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['containers', 'indexNextContainer'], output_keys=['containerPos'])

        with _sm_getunseencontainer_10:
            # x:79 y:27
            OperatableStateMachine.add('getContainerId',
                                        FlexibleCalculationState(calculation=lambda x: x[0][x[1]], input_keys=['containers','indexNextContainer']),
                                        transitions={'done': 'getContainerFromWonderland'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'containers': 'containers', 'indexNextContainer': 'indexNextContainer', 'output_value': 'containerId'})

            # x:312 y:121
            OperatableStateMachine.add('CouldntFindContainer',
                                        SaraSay(sentence=lambda x:"Couldnt Find Container "+x, input_keys=['containerId'], emotion=0, block=True),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'containerId': 'containerId'})

            # x:82 y:232
            OperatableStateMachine.add('getContainerPos',
                                        CalculationState(calculation=lambda x: x.position),
                                        transitions={'done': 'IncrementIndexNextContainer'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'entity', 'output_value': 'containerPos'})

            # x:67 y:122
            OperatableStateMachine.add('getContainerFromWonderland',
                                        WonderlandGetEntityByID(),
                                        transitions={'found': 'getContainerPos', 'not_found': 'CouldntFindContainer', 'error': 'CouldntFindContainer'},
                                        autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off, 'error': Autonomy.Off},
                                        remapping={'id': 'containerId', 'entity': 'entity', 'depth_position': 'depth_position', 'depth_waypoint': 'depth_waypoint'})

            # x:64 y:371
            OperatableStateMachine.add('IncrementIndexNextContainer',
                                        CalculationState(calculation=lambda x: x+1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'indexNextContainer', 'output_value': 'indexNextContainer'})


        # x:130 y:465, x:230 y:465
        _sm_getlastseenobject_11 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['seenObjects'], output_keys=['seenObj'])

        with _sm_getlastseenobject_11:
            # x:92 y:40
            OperatableStateMachine.add('getLatestSeenObject',
                                        CalculationState(calculation=lambda x: x[-1]),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'seenObjects', 'output_value': 'seenObj'})


        # x:73 y:459, x:263 y:464
        _sm_hascontainerleft_12 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['containers', 'indexNextContainer'])

        with _sm_hascontainerleft_12:
            # x:46 y:33
            OperatableStateMachine.add('len(containers) > indexNextContainer',
                                        FlexibleCalculationState(calculation=lambda x: len(x[0]) > x[1], input_keys=['containers','indexNextContainer']),
                                        transitions={'done': 'IsIndexNextContainerInBounds'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'containers': 'containers', 'indexNextContainer': 'indexNextContainer', 'output_value': 'cond'})

            # x:50 y:150
            OperatableStateMachine.add('IsIndexNextContainerInBounds',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x: (x) ? 'done' : 'failed'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'cond'})


        # x:130 y:465, x:230 y:465
        _sm_hasseenobject_13 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['seenObjects'])

        with _sm_hasseenobject_13:
            # x:74 y:25
            OperatableStateMachine.add('getSeenObjectsLength',
                                        CalculationState(calculation=lambda x: len(x)),
                                        transitions={'done': 'isLengthNotZero'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'input_value': 'seenObjects', 'output_value': 'length'})

            # x:157 y:174
            OperatableStateMachine.add('isLengthNotZero',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x: (x > 0) ? 'done' : 'failed'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'length'})


        # x:130 y:465, x:230 y:465
        _sm_mainloop_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_mainloop_14:
            # x:98 y:96
            OperatableStateMachine.add('02',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_enterarena_15 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_enterarena_15:
            # x:98 y:96
            OperatableStateMachine.add('01',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})



        with _state_machine:
            # x:55 y:28
            OperatableStateMachine.add('EnterArena',
                                        _sm_enterarena_15,
                                        transitions={'done': 'MainLoop', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:55 y:143
            OperatableStateMachine.add('MainLoop',
                                        _sm_mainloop_14,
                                        transitions={'done': 'hasSeenObject', 'failed': 'hasSeenObject'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:53 y:240
            OperatableStateMachine.add('hasSeenObject',
                                        _sm_hasseenobject_13,
                                        transitions={'done': 'GetLastSeenObject', 'failed': 'hasContainerLeft'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'seenObjects': 'seenObjects'})

            # x:237 y:2
            OperatableStateMachine.add('hasContainerLeft',
                                        _sm_hascontainerleft_12,
                                        transitions={'done': 'GetUnseenContainer', 'failed': 'sayDone'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'containers': 'containers', 'indexNextContainer': 'indexNextContainer'})

            # x:45 y:338
            OperatableStateMachine.add('GetLastSeenObject',
                                        _sm_getlastseenobject_11,
                                        transitions={'done': 'GotoWhileLooking', 'failed': 'GetUnseenContainer'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'seenObjects': 'seenObjects', 'seenObj': 'seenObj'})

            # x:229 y:79
            OperatableStateMachine.add('GetUnseenContainer',
                                        _sm_getunseencontainer_10,
                                        transitions={'done': 'GotoWhileLooking', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'containers': 'containers', 'indexNextContainer': 'indexNextContainer', 'containerPos': 'containerPos'})

            # x:235 y:181
            OperatableStateMachine.add('GotoWhileLooking',
                                        _sm_gotowhilelooking_9,
                                        transitions={'done': 'ScanContainer', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:239 y:266
            OperatableStateMachine.add('ScanContainer',
                                        _sm_scancontainer_8,
                                        transitions={'done': 'GrabClosestObject', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:233 y:375
            OperatableStateMachine.add('GrabClosestObject',
                                        _sm_grabclosestobject_7,
                                        transitions={'done': 'GotoDesiredContainer', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:229 y:479
            OperatableStateMachine.add('GotoDesiredContainer',
                                        _sm_gotodesiredcontainer_6,
                                        transitions={'done': 'PutDownObject', 'failed': 'AskForHelp'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:550 y:14
            OperatableStateMachine.add('PutDownObject',
                                        _sm_putdownobject_5,
                                        transitions={'done': 'continueLoop', 'failed': 'SayYouMissedYourShot'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'containerPos': 'containerPos'})

            # x:775 y:16
            OperatableStateMachine.add('SayYouMissedYourShot',
                                        _sm_sayyoumissedyourshot_4,
                                        transitions={'done': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:510 y:411
            OperatableStateMachine.add('AskForHelp',
                                        _sm_askforhelp_3,
                                        transitions={'done': 'ComplexBehaviorForDeusExMachina', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:683 y:408
            OperatableStateMachine.add('ComplexBehaviorForDeusExMachina',
                                        _sm_complexbehaviorfordeusexmachina_2,
                                        transitions={'done': 'continueLoop', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': '___'})

            # x:530 y:143
            OperatableStateMachine.add('continueLoop',
                                        _sm_continueloop_1,
                                        transitions={'done': 'MainLoop'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:883 y:116
            OperatableStateMachine.add('sayDone',
                                        _sm_saydone_0,
                                        transitions={'done': 'done', 'failed': 'done'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'indexNextContainer': 'indexNextContainer'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
