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

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
    
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1200 y:570, x:5 y:103
        _state_machine = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])
        _state_machine.userdata.input_value = ''

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:130 y:465, x:230 y:465
        _sm_saydone_0 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_saydone_0:
            # x:98 y:96
            OperatableStateMachine.add('018',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_sayyoulostyourwaytothecenter_1 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_sayyoulostyourwaytothecenter_1:
            # x:98 y:96
            OperatableStateMachine.add('017',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_continueloop_2 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_continueloop_2:
            # x:98 y:96
            OperatableStateMachine.add('016',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_retry3times_3 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_retry3times_3:
            # x:98 y:96
            OperatableStateMachine.add('015',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_complexbehaviorfordeusexmachina_4 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_complexbehaviorfordeusexmachina_4:
            # x:98 y:96
            OperatableStateMachine.add('014',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_askforhelp_5 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_askforhelp_5:
            # x:98 y:96
            OperatableStateMachine.add('013',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_sayyoumissedyourshot_6 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_sayyoumissedyourshot_6:
            # x:98 y:96
            OperatableStateMachine.add('012',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_putdownobject_7 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_putdownobject_7:
            # x:98 y:96
            OperatableStateMachine.add('011',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_gotodesiredcontainer_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_gotodesiredcontainer_8:
            # x:98 y:96
            OperatableStateMachine.add('010',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_grabclosestobject_9 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_grabclosestobject_9:
            # x:98 y:96
            OperatableStateMachine.add('09',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_scancontainer_10 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_scancontainer_10:
            # x:98 y:96
            OperatableStateMachine.add('08',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_gotowhilelooking_11 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_gotowhilelooking_11:
            # x:98 y:96
            OperatableStateMachine.add('07',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_getunseencontainer_12 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_getunseencontainer_12:
            # x:98 y:96
            OperatableStateMachine.add('06',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_getlastseenobject_13 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_getlastseenobject_13:
            # x:98 y:96
            OperatableStateMachine.add('05',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_hascontainerleft_14 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_hascontainerleft_14:
            # x:98 y:96
            OperatableStateMachine.add('04',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_hasseenobject_15 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_hasseenobject_15:
            # x:98 y:96
            OperatableStateMachine.add('03',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_mainloop_16 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_mainloop_16:
            # x:98 y:96
            OperatableStateMachine.add('02',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})


        # x:130 y:465, x:230 y:465
        _sm_enterarena_17 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['input_value'])

        with _sm_enterarena_17:
            # x:98 y:96
            OperatableStateMachine.add('01',
                                        DecisionState(outcomes=['done','failed'], conditions=lambda x:'done'),
                                        transitions={'done': 'done', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'input_value': 'input_value'})



        with _state_machine:
            # x:55 y:28
            OperatableStateMachine.add('EnterArena',
                                        _sm_enterarena_17,
                                        transitions={'done': 'MainLoop', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:8 y:137
            OperatableStateMachine.add('MainLoop',
                                        _sm_mainloop_16,
                                        transitions={'done': 'hasSeenObject', 'failed': 'hasSeenObject'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:53 y:211
            OperatableStateMachine.add('hasSeenObject',
                                        _sm_hasseenobject_15,
                                        transitions={'done': 'GetLastSeenObject', 'failed': 'hasContainerLeft'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:237 y:20
            OperatableStateMachine.add('hasContainerLeft',
                                        _sm_hascontainerleft_14,
                                        transitions={'done': 'GetUnseenContainer', 'failed': 'sayDone'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:45 y:289
            OperatableStateMachine.add('GetLastSeenObject',
                                        _sm_getlastseenobject_13,
                                        transitions={'done': 'GotoWhileLooking', 'failed': 'GetUnseenContainer'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:225 y:97
            OperatableStateMachine.add('GetUnseenContainer',
                                        _sm_getunseencontainer_12,
                                        transitions={'done': 'GotoWhileLooking', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:236 y:172
            OperatableStateMachine.add('GotoWhileLooking',
                                        _sm_gotowhilelooking_11,
                                        transitions={'done': 'ScanContainer', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:238 y:251
            OperatableStateMachine.add('ScanContainer',
                                        _sm_scancontainer_10,
                                        transitions={'done': 'GrabClosestObject', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:232 y:328
            OperatableStateMachine.add('GrabClosestObject',
                                        _sm_grabclosestobject_9,
                                        transitions={'done': 'GotoDesiredContainer', 'failed': 'Retry3Times'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:229 y:399
            OperatableStateMachine.add('GotoDesiredContainer',
                                        _sm_gotodesiredcontainer_8,
                                        transitions={'done': 'PutDownObject', 'failed': 'AskForHelp'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:404 y:15
            OperatableStateMachine.add('PutDownObject',
                                        _sm_putdownobject_7,
                                        transitions={'done': 'continueLoop', 'failed': 'SayYouMissedYourShot'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:658 y:15
            OperatableStateMachine.add('SayYouMissedYourShot',
                                        _sm_sayyoumissedyourshot_6,
                                        transitions={'done': 'continueLoop', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:510 y:411
            OperatableStateMachine.add('AskForHelp',
                                        _sm_askforhelp_5,
                                        transitions={'done': 'ComplexBehaviorForDeusExMachina', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:683 y:408
            OperatableStateMachine.add('ComplexBehaviorForDeusExMachina',
                                        _sm_complexbehaviorfordeusexmachina_4,
                                        transitions={'done': 'continueLoop', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:414 y:293
            OperatableStateMachine.add('Retry3Times',
                                        _sm_retry3times_3,
                                        transitions={'done': 'GrabClosestObject', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:530 y:143
            OperatableStateMachine.add('continueLoop',
                                        _sm_continueloop_2,
                                        transitions={'done': 'MainLoop', 'failed': 'SayYouLostYourWayToTheCenter'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:712 y:221
            OperatableStateMachine.add('SayYouLostYourWayToTheCenter',
                                        _sm_sayyoulostyourwaytothecenter_1,
                                        transitions={'done': 'continueLoop', 'failed': 'continueLoop'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})

            # x:705 y:114
            OperatableStateMachine.add('sayDone',
                                        _sm_saydone_0,
                                        transitions={'done': 'done', 'failed': 'done'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'input_value': 'input_value'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
