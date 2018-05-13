#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario2_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_sound import SaraSound
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.door_detector import DoorDetector
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 12 mai 2018
@author: Veronica Romero
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
        # x:1166 y:631
        _state_machine = OperatableStateMachine(outcomes=['finished'])
        _state_machine.userdata.relative = True

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]


        with _state_machine:
            # x:77 y:128
            OperatableStateMachine.add('set not relative',
                                        SetKey(Value=False),
                                        transitions={'done': 'wait to start (door open)'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'Key': 'relative'})

            # x:365 y:449
            OperatableStateMachine.add('Bouton continuer',
                                        ContinueButton(),
                                        transitions={'true': 'Gen test zone exit', 'false': 'Waiting'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

            # x:37 y:612
            OperatableStateMachine.add('Failed',
                                        SaraSound(sound="error.wav"),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:26 y:299
            OperatableStateMachine.add('Gen test zone position',
                                        GenPoseEuler(x=1.27, y=-5.7165979361, z=0, roll=0, pitch=0, yaw=90),
                                        transitions={'done': 'Moving'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:750 y:430
            OperatableStateMachine.add('Move to exit door',
                                        self.use_behavior(Action_MoveSM, 'Move to exit door'),
                                        transitions={'finished': 'wait for door to open', 'failed': 'Door not found'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:746 y:737
            OperatableStateMachine.add('Move GTFO (get out)',
                                        self.use_behavior(Action_MoveSM, 'Move GTFO (get out)'),
                                        transitions={'finished': 'finished', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:303 y:221
            OperatableStateMachine.add('Waiting message',
                                        SaraSay(sentence="Waiting for the door to open", emotion=1, block=True),
                                        transitions={'done': 'wait to start (door open)'},
                                        autonomy={'done': Autonomy.Off})

            # x:921 y:463
            OperatableStateMachine.add('wait for door to open',
                                        DoorDetector(timeout=1500),
                                        transitions={'done': 'gen exit pos', 'failed': 'Door not found'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:378 y:523
            OperatableStateMachine.add('Waiting',
                                        SaraSound(sound="to_be_continued.wav"),
                                        transitions={'done': 'Bouton continuer'},
                                        autonomy={'done': Autonomy.Off})

            # x:520 y:445
            OperatableStateMachine.add('Gen test zone exit',
                                        GenPoseEuler(x=2.26782121774, y=-6.1888976361, z=0, roll=0, pitch=0, yaw=0),
                                        transitions={'done': 'Exit zone'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:1142 y:386
            OperatableStateMachine.add('Door not found',
                                        SaraSay(sentence="Sorry, I did not found the doord", emotion=1, block=True),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off})

            # x:20 y:456
            OperatableStateMachine.add('Move to test zone',
                                        self.use_behavior(Action_MoveSM, 'Move to test zone'),
                                        transitions={'finished': 'say ready', 'failed': 'Failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'pose': 'pose', 'relative': 'relative'})

            # x:93 y:26
            OperatableStateMachine.add('Bouton to start',
                                        ContinueButton(),
                                        transitions={'true': 'set not relative', 'false': 'Bouton to start'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

            # x:931 y:570
            OperatableStateMachine.add('gen exit pos',
                                        GenPoseEuler(x=3, y=-6.1888976361, z=0, roll=0, pitch=0, yaw=0),
                                        transitions={'done': 'Move GTFO (get out)'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'pose': 'pose'})

            # x:27 y:216
            OperatableStateMachine.add('wait to start (door open)',
                                        DoorDetector(timeout=15000),
                                        transitions={'done': 'Gen test zone position', 'failed': 'Waiting message'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:229 y:453
            OperatableStateMachine.add('say ready',
                                        SaraSay(sentence="I'm ready for my safety check", emotion=1, block=True),
                                        transitions={'done': 'Bouton continuer'},
                                        autonomy={'done': Autonomy.Off})

            # x:40 y:373
            OperatableStateMachine.add('Moving',
                                        SaraSay(sentence="Moving to the test zone", emotion=1, block=True),
                                        transitions={'done': 'Move to test zone'},
                                        autonomy={'done': Autonomy.Off})

            # x:655 y:436
            OperatableStateMachine.add('Exit zone',
                                        SaraSay(sentence="Moving to the exit door", emotion=1, block=True),
                                        transitions={'done': 'Move to exit door'},
                                        autonomy={'done': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
