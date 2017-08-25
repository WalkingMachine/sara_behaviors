#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_presentation')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.regex_tester import RegexTester
from behavior_get_speech.get_speech_sm import Get_speechSM
from sara_flexbe_states.sara_sound import SaraSound
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Aug 24 2017
@author: PLM, MSTP
'''
class Sara_presentationSM(Behavior):
    '''
    laisse sara se presenter
    '''


    def __init__(self):
        super(Sara_presentationSM, self).__init__()
        self.name = 'Sara_presentation'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(Get_speechSM, 'Greet/Get name/Get_speech')
        self.add_behavior(Get_speechSM, 'Greet/Get name/Get_speech_2')
        self.add_behavior(Get_speechSM, 'questions/Get_speech')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:624 y:423, x:621 y:334
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.name = ""

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:409 y:239, x:481 y:479
        _sm_get_name_0 = OperatableStateMachine(outcomes=['unavailable', 'true'], output_keys=['name'])

        with _sm_get_name_0:
            # x:56 y:40
            OperatableStateMachine.add('ask for name',
                                        SaraSay(sentence="what is your name", emotion=1),
                                        transitions={'done': 'play pign'},
                                        autonomy={'done': Autonomy.Off})

            # x:51 y:283
            OperatableStateMachine.add('say name',
                                        SaraSayKey(Format=lambda x: "Did you say your name was "+x+"?", emotion=1),
                                        transitions={'done': 'wait4'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:237 y:96
            OperatableStateMachine.add('wait3',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'play pign'},
                                        autonomy={'done': Autonomy.Off})

            # x:256 y:467
            OperatableStateMachine.add('check responce',
                                        RegexTester(regex=".*([Yy]es).*"),
                                        transitions={'true': 'true', 'false': 'ask for name'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'validation', 'result': 'result'})

            # x:56 y:363
            OperatableStateMachine.add('wait4',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'Get_speech_2'},
                                        autonomy={'done': Autonomy.Off})

            # x:45 y:192
            OperatableStateMachine.add('Get_speech',
                                        self.use_behavior(Get_speechSM, 'Greet/Get name/Get_speech'),
                                        transitions={'finished': 'say name', 'failed': 'unavailable'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'words': 'name'})

            # x:28 y:464
            OperatableStateMachine.add('Get_speech_2',
                                        self.use_behavior(Get_speechSM, 'Greet/Get name/Get_speech_2'),
                                        transitions={'finished': 'check responce', 'failed': 'unavailable'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'words': 'validation'})

            # x:63 y:119
            OperatableStateMachine.add('play pign',
                                        SaraSound(sound="ding.wav"),
                                        transitions={'done': 'Get_speech'},
                                        autonomy={'done': Autonomy.Off})


        # x:753 y:132, x:562 y:607
        _sm_questions_1 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name'])

        with _sm_questions_1:
            # x:44 y:39
            OperatableStateMachine.add('ask for questions',
                                        SaraSay(sentence="ask a question", emotion=1),
                                        transitions={'done': 'wait1'},
                                        autonomy={'done': Autonomy.Off})

            # x:53 y:122
            OperatableStateMachine.add('wait1',
                                        WaitState(wait_time=2),
                                        transitions={'done': 'Get_speech'},
                                        autonomy={'done': Autonomy.Off})

            # x:540 y:552
            OperatableStateMachine.add('if gripper',
                                        RegexTester(regex=".*([Gg]ripper)|([Hh]and)|([Cc]law).*"),
                                        transitions={'true': 'respond gripper', 'false': 'if base'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:292 y:536
            OperatableStateMachine.add('respond gripper',
                                        SaraSay(sentence="My gripper is bla bla bla", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:542 y:472
            OperatableStateMachine.add('if base',
                                        RegexTester(regex=".*([Bb]ase)|([Ww]heels)|([Bb]ottom)|([Ll]egs)|([Mm]ove).*"),
                                        transitions={'true': 'respond base', 'false': 'if brain'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:299 y:470
            OperatableStateMachine.add('respond base',
                                        SaraSay(sentence="My base is bla bla bla", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:561 y:76
            OperatableStateMachine.add('Sorry',
                                        SaraSay(sentence="sorry I did not understand", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:42 y:573
            OperatableStateMachine.add('Get_speech',
                                        self.use_behavior(Get_speechSM, 'questions/Get_speech'),
                                        transitions={'finished': 'if gripper', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'words': 'question'})

            # x:548 y:160
            OperatableStateMachine.add('Stop',
                                        RegexTester(regex=".*([Ss]top)|([Oo]ver)|([Dd]one)|([Ff]inish).*"),
                                        transitions={'true': 'done', 'false': 'Sorry'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:549 y:239
            OperatableStateMachine.add('if head',
                                        RegexTester(regex=".*([Hh]ead)|([Ss]houlder)|([Ff]ace).*"),
                                        transitions={'true': 'say head', 'false': 'Stop'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:547 y:318
            OperatableStateMachine.add('if arm',
                                        RegexTester(regex=".*([Aa]rm)|([Mm]uscle).*"),
                                        transitions={'true': 'say arm', 'false': 'if head'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:544 y:396
            OperatableStateMachine.add('if brain',
                                        RegexTester(regex=".*([Bb]rain)|([Cc]ompute)|([Ll]aptop).*"),
                                        transitions={'true': 'say brain', 'false': 'if arm'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:314 y:396
            OperatableStateMachine.add('say brain',
                                        SaraSay(sentence="my brain is blah blah blah", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:322 y:320
            OperatableStateMachine.add('say arm',
                                        SaraSay(sentence="my arm is blah blah blah", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:321 y:245
            OperatableStateMachine.add('say head',
                                        SaraSay(sentence="my head is blah blah blah", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})


        # x:294 y:283, x:283 y:499
        _sm_greet_2 = OperatableStateMachine(outcomes=['unavailable', 'done'], output_keys=['name'])

        with _sm_greet_2:
            # x:48 y:40
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'say hello'},
                                        autonomy={'done': Autonomy.Off})

            # x:47 y:114
            OperatableStateMachine.add('say hello',
                                        SaraSay(sentence="Hello", emotion=1),
                                        transitions={'done': 'wait2'},
                                        autonomy={'done': Autonomy.Off})

            # x:46 y:183
            OperatableStateMachine.add('wait2',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'Get name'},
                                        autonomy={'done': Autonomy.Off})

            # x:50 y:492
            OperatableStateMachine.add('wait4',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})

            # x:34 y:269
            OperatableStateMachine.add('Get name',
                                        _sm_get_name_0,
                                        transitions={'unavailable': 'unavailable', 'true': 'say greet'},
                                        autonomy={'unavailable': Autonomy.Inherit, 'true': Autonomy.Inherit},
                                        remapping={'name': 'name'})

            # x:44 y:382
            OperatableStateMachine.add('say greet',
                                        SaraSayKey(Format=lambda x: "greetings "+x, emotion=1),
                                        transitions={'done': 'wait4'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})



        with _state_machine:
            # x:60 y:32
            OperatableStateMachine.add('Greet',
                                        _sm_greet_2,
                                        transitions={'unavailable': 'failed', 'done': 'questions'},
                                        autonomy={'unavailable': Autonomy.Inherit, 'done': Autonomy.Inherit},
                                        remapping={'name': 'name'})

            # x:60 y:164
            OperatableStateMachine.add('questions',
                                        _sm_questions_1,
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'name': 'name'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
