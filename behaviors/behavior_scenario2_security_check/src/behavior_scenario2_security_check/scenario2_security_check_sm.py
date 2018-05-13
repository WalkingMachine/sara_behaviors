#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario2_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.door_detector import DoorDetector
from sara_flexbe_states.sara_sound import SaraSound
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 12 mai 2018
@author: Véronica Romero
'''
class Scenario2_Security_CheckSM(Behavior):
    '''
    englobe le scenario du test de securite.
    '''


    def __init__(self):
        super(Scenario2_Security_CheckSM, self).__init__()
        self.name = 'Scenario2_Security_Check'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Action_MoveSM, 'Move to exit door')
        self.add_behavior(Action_MoveSM, 'Move GTFO (get out)')
        self.add_behavior(Action_MoveSM, 'Move to test zone')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:1028 y:448
        _state_machine = OperatableStateMachine(outcomes=['finished'])
        _state_machine.userdata.relative = []
        _state_machine.userdata.Door = true

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:26 y:98
            OperatableStateMachine.add('wait to start (door open)',
                                        DoorDetector(timeout=15000),
                                        transitions={'done': 'Gen test zone position', 'failed': 'Waiting message'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:351 y:274
            OperatableStateMachine.add('Bouton continuer',
                                        ContinueButton(),
                                        transitions={'true': 'Gen test zone exit', 'false': 'Waiting'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

            # x:37 y:442
            OperatableStateMachine.add('Failed',
                                        SaraSound(sound="error.wav"),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:210 y:278
            OperatableStateMachine.add('Wait to continue',
                                        WaitState(wait_time=15000),
                                        transitions={'done': 'Bouton continuer'},
                                        autonomy={'done': Autonomy.Off})

            # x:23 y:176
            OperatableStateMachine.add('Gen test zone position',
                                        GenPoseEuler(x=0, y=0, z=0, roll=0, pitch=0, yaw=90),
                                        transitions={'done': 'Move to test zone'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:635 y:256
            OperatableStateMachine.add('Move to exit door',
                                        self.use_behavior(Action_MoveSM, 'Move to exit door'),
                                        transitions={'finished': 'wait for door to open', 'failed': 'Door not found'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:810 y:386
            OperatableStateMachine.add('Move GTFO (get out)',
                                        self.use_behavior(Action_MoveSM, 'Move GTFO (get out)'),
                                        transitions={'finished': 'finished', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:234 y:88
            OperatableStateMachine.add('Waiting message',
                                        SaraSay(sentence="Waiting for the door to open", emotion=1, block=True),
                                        transitions={'done': 'wait to start (door open)'},
                                        autonomy={'done': Autonomy.Off})

            # x:822 y:247
            OperatableStateMachine.add('wait for door to open',
                                        DoorDetector(timeout=1500),
                                        transitions={'done': 'Move GTFO (get out)', 'failed': 'Door not found'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:361 y:358
            OperatableStateMachine.add('Waiting',
                                        SaraSound(sound="to_be_continued.wav"),
                                        transitions={'done': 'Bouton continuer'},
                                        autonomy={'done': Autonomy.Off})

            # x:489 y:268
            OperatableStateMachine.add('Gen test zone exit',
                                        GenPoseEuler(x=0, y=0, z=0, roll=0, pitch=0, yaw=90),
                                        transitions={'done': 'Move to exit door'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:651 y:344
            OperatableStateMachine.add('Door not found',
                                        SaraSay(sentence="Sorry, I did not found the doord", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:21 y:274
            OperatableStateMachine.add('Move to test zone',
                                        self.use_behavior(Action_MoveSM, 'Move to test zone'),
                                        transitions={'finished': 'Wait to continue', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:93 y:26
            OperatableStateMachine.add('Bouton to start',
                                        ContinueButton(),
                                        transitions={'true': 'wait to start (door open)', 'false': 'Bouton to start'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
