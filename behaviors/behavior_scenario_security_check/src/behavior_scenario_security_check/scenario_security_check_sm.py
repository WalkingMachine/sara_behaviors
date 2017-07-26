#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_wonderland_get_waypoint.wonderland_get_waypoint_sm import Wonderland_Get_WaypointSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.continue_button import ContinueButton
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.door_detector import DoorDetector
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
        self.add_behavior(Wonderland_Get_WaypointSM, 'go to test waypoint/Wonderland_Get_Waypoint')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:790 y:491, x:429 y:316
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.waypoint = []
        _state_machine.userdata.waypoint_name = ""
        _state_machine.userdata.waypoint_exit = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:889 y:108
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

            # x:621 y:187
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


        # x:30 y:308, x:130 y:308
        _sm_go_to_exit_1 = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _sm_go_to_exit_1:
            # x:54 y:153
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})


        # x:846 y:86, x:830 y:283
        _sm_go_to_test_waypoint_2 = OperatableStateMachine(outcomes=['arrived', 'failed'], input_keys=['waypoint_name'])

        with _sm_go_to_test_waypoint_2:
            # x:141 y:49
            OperatableStateMachine.add('Wonderland_Get_Waypoint',
                                        self.use_behavior(Wonderland_Get_WaypointSM, 'go to test waypoint/Wonderland_Get_Waypoint'),
                                        transitions={'finished': 'move the robot', 'failed': 'Sorry no waypoint'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'name': 'waypoint_name', 'waypoint': 'waypoint'})

            # x:169 y:276
            OperatableStateMachine.add('Sorry no waypoint',
                                        SaraSay(sentence="Sorry, I don't know where to go.", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})

            # x:469 y:181
            OperatableStateMachine.add('error',
                                        SaraSay(sentence="Sorry, I seem to have trouble with my navigation system", emotion=1),
                                        transitions={'done': 'failed'},
                                        autonomy={'done': Autonomy.Off})

            # x:453 y:49
            OperatableStateMachine.add('move the robot',
                                        SaraMoveBase(),
                                        transitions={'arrived': 'arrived', 'failed': 'error'},
                                        autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'pose': 'waypoint'})



        with _state_machine:
            # x:75 y:302
            OperatableStateMachine.add('go to test waypoint',
                                        _sm_go_to_test_waypoint_2,
                                        transitions={'arrived': 'wait for continue button', 'failed': 'failed'},
                                        autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'waypoint_name': 'waypoint_name'})

            # x:84 y:482
            OperatableStateMachine.add('wait for continue button',
                                        ContinueButton(),
                                        transitions={'Continue': 'go to exit', 'wait': 'wait for continue button'},
                                        autonomy={'Continue': Autonomy.Off, 'wait': Autonomy.Off})

            # x:393 y:473
            OperatableStateMachine.add('go to exit',
                                        _sm_go_to_exit_1,
                                        transitions={'finished': 'finished', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:75 y:130
            OperatableStateMachine.add('Door management',
                                        _sm_door_management_0,
                                        transitions={'done': 'go to test waypoint'},
                                        autonomy={'done': Autonomy.Inherit})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
