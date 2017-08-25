#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_sara_presentation')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.sara_start_face import StartFace
from sara_flexbe_states.sara_say_key import SaraSayKey
from sara_flexbe_states.regex_tester import RegexTester
from sara_flexbe_states.sara_say import SaraSay
from behavior_get_speech.get_speech_sm import Get_speechSM
from sara_flexbe_states.sara_sound import SaraSound
from sara_flexbe_states.move_joint import MoveJoint
from sara_flexbe_states.publisher_gripper_state import PublisherGripperState
from sara_flexbe_states.unit8_topic_publisher import PublishUint8
from flexbe_states.wait_state import WaitState
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
        self.add_behavior(Get_speechSM, 'questions/Get_speech')
        self.add_behavior(Get_speechSM, 'Greet/Get name/Get_speech')
        self.add_behavior(Get_speechSM, 'Greet/Get name/Get_speech_2')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]
        
        # [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:624 y:423, x:621 y:334
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
        _state_machine.userdata.name = "you"
        _state_machine.userdata.widthclose = 0
        _state_machine.userdata.widthopen = 250
        _state_machine.userdata.effort = 100
        _state_machine.userdata.topicface = "/sara_face/Emotion"
        _state_machine.userdata.happy = 1
        _state_machine.userdata.wink = 6
        _state_machine.userdata.surprise = 5
        _state_machine.userdata.lowmouth = 3

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

        # x:479 y:319, x:481 y:479
        _sm_get_name_0 = OperatableStateMachine(outcomes=['unavailable', 'true'], input_keys=['topicface', 'surprise', 'lowmouth', 'happy'], output_keys=['name'])

        with _sm_get_name_0:
            # x:56 y:40
            OperatableStateMachine.add('ask for name',
                                        SaraSay(sentence="Just say your name after the beep sound", emotion=1),
                                        transitions={'done': 'play pign'},
                                        autonomy={'done': Autonomy.Off})

            # x:51 y:283
            OperatableStateMachine.add('say name',
                                        SaraSayKey(Format=lambda x: "Did you say your name was "+x+"?", emotion=1),
                                        transitions={'done': 'wait4'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:256 y:467
            OperatableStateMachine.add('check responce',
                                        RegexTester(regex=".*(([Yy]es)|([Yy]ea)|([Ss]ure)|([Ii]ndeed)).*"),
                                        transitions={'true': 'true', 'false': 'low'},
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

            # x:217 y:259
            OperatableStateMachine.add('sorry',
                                        SaraSay(sentence="Sorry, I'm not good with names. Just say your name again after the beep sound.", emotion=1),
                                        transitions={'done': 'happy'},
                                        autonomy={'done': Autonomy.Off})

            # x:234 y:356
            OperatableStateMachine.add('low',
                                        PublishUint8(),
                                        transitions={'done': 'sorry'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'topic': 'topicface', 'data': 'lowmouth'})

            # x:180 y:114
            OperatableStateMachine.add('happy',
                                        PublishUint8(),
                                        transitions={'done': 'play pign'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'topic': 'topicface', 'data': 'happy'})


        # x:277 y:519
        _sm_show_gripper_1 = OperatableStateMachine(outcomes=['done'], input_keys=['widthopen', 'widthclosed', 'effort'])

        with _sm_show_gripper_1:
            # x:30 y:40
            OperatableStateMachine.add('respond gripper',
                                        SaraSay(sentence="My gripper is build by Robotiq and allows me to pick up things.", emotion=1),
                                        transitions={'done': 'close'},
                                        autonomy={'done': Autonomy.Off})

            # x:38 y:214
            OperatableStateMachine.add('close',
                                        PublisherGripperState(),
                                        transitions={'done': 'say catch'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'width': 'widthclosed', 'effort': 'effort'})

            # x:55 y:506
            OperatableStateMachine.add('open',
                                        PublisherGripperState(),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'width': 'widthopen', 'effort': 'effort'})

            # x:63 y:389
            OperatableStateMachine.add('say catch',
                                        SaraSay(sentence="I am an excellent catch", emotion=1),
                                        transitions={'done': 'open'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:325
        _sm_show_base_2 = OperatableStateMachine(outcomes=['done'])

        with _sm_show_base_2:
            # x:30 y:40
            OperatableStateMachine.add('respond base',
                                        SaraSay(sentence="My base is what allows me to move. I can go in any direction thanks to my mecanum wheels and motor controllers.", emotion=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:325
        _sm_show_brain_3 = OperatableStateMachine(outcomes=['done'])

        with _sm_show_brain_3:
            # x:30 y:40
            OperatableStateMachine.add('say brain',
                                        SaraSay(sentence="My brain is located inside my laptop. You can call me a no brainer.", emotion=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:92 y:333
        _sm_show_arm_4 = OperatableStateMachine(outcomes=['done'])

        with _sm_show_arm_4:
            # x:75 y:37
            OperatableStateMachine.add('say arm',
                                        SaraSay(sentence="My arm is custom made from 3d printed titanium and use Kinova harmonic drives to move.", emotion=1),
                                        transitions={'done': 'move to idle'},
                                        autonomy={'done': Autonomy.Off})

            # x:65 y:130
            OperatableStateMachine.add('move to idle',
                                        MoveJoint(pose_name="IdlePose"),
                                        transitions={'done': 'say cap', 'failed': 'say cap'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:68 y:220
            OperatableStateMachine.add('say cap',
                                        SaraSay(sentence="With these, I can lift up to 2 pounds of weight.", emotion=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:30 y:325
        _sm_show_head_5 = OperatableStateMachine(outcomes=['done'])

        with _sm_show_head_5:
            # x:30 y:40
            OperatableStateMachine.add('say head',
                                        SaraSay(sentence="my head is blah blah blah", emotion=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})


        # x:294 y:283, x:283 y:499
        _sm_greet_6 = OperatableStateMachine(outcomes=['unavailable', 'done'], input_keys=['topicface', 'happy', 'surprise', 'lowmouth'], output_keys=['name'])

        with _sm_greet_6:
            # x:48 y:40
            OperatableStateMachine.add('wait',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'face happy'},
                                        autonomy={'done': Autonomy.Off})

            # x:47 y:114
            OperatableStateMachine.add('say hello',
                                        SaraSay(sentence="Hi, my name is sarah. I am a human assistant robot made by the student club Walking Machine of ETS.  This presentation is  interactive. To stop this presentation at anytime say stop.", emotion=1),
                                        transitions={'done': 'wait2'},
                                        autonomy={'done': Autonomy.Off})

            # x:46 y:183
            OperatableStateMachine.add('wait2',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'call name'},
                                        autonomy={'done': Autonomy.Off})

            # x:50 y:492
            OperatableStateMachine.add('wait4',
                                        WaitState(wait_time=1),
                                        transitions={'done': 'done'},
                                        autonomy={'done': Autonomy.Off})

            # x:32 y:336
            OperatableStateMachine.add('Get name',
                                        _sm_get_name_0,
                                        transitions={'unavailable': 'unavailable', 'true': 'say greet'},
                                        autonomy={'unavailable': Autonomy.Inherit, 'true': Autonomy.Inherit},
                                        remapping={'topicface': 'topicface', 'surprise': 'surprise', 'lowmouth': 'lowmouth', 'happy': 'happy', 'name': 'name'})

            # x:44 y:419
            OperatableStateMachine.add('say greet',
                                        SaraSayKey(Format=lambda x: "Nice to meet you "+x+". I am happy to see you today. We never get visitors around here.", emotion=1),
                                        transitions={'done': 'wait4'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:51 y:261
            OperatableStateMachine.add('call name',
                                        SaraSay(sentence="Before we start, could you tell me your name please?", emotion=1),
                                        transitions={'done': 'Get name'},
                                        autonomy={'done': Autonomy.Off})

            # x:196 y:114
            OperatableStateMachine.add('face happy',
                                        PublishUint8(),
                                        transitions={'done': 'say hello'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'topic': 'topicface', 'data': 'happy'})


        # x:930 y:175, x:217 y:461
        _sm_questions_7 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name', 'widthopen', 'widthclosed', 'effort', 'topicface', 'lowmouth', 'happy'])

        with _sm_questions_7:
            # x:55 y:43
            OperatableStateMachine.add('say question',
                                        SaraSayKey(Format=lambda x: "Now "+x+". You can ask me about my head, arm, hand, base, wheel and brain. I am almost like a human but better.", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:631 y:530
            OperatableStateMachine.add('if gripper',
                                        RegexTester(regex=".*([Gg]ripper)|([Hh]and)|([Cc]law).*"),
                                        transitions={'true': 'show gripper', 'false': 'if base'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:635 y:457
            OperatableStateMachine.add('if base',
                                        RegexTester(regex=".*(([Bb]ase)|([Ww]heel)|([Bb]ottom)|([Ll]egs)|([Mm]ove)).*"),
                                        transitions={'true': 'show base', 'false': 'if brain'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:382 y:88
            OperatableStateMachine.add('Sorry',
                                        SaraSay(sentence="sorry I did not understand", emotion=1),
                                        transitions={'done': 'happy'},
                                        autonomy={'done': Autonomy.Off})

            # x:42 y:548
            OperatableStateMachine.add('Get_speech',
                                        self.use_behavior(Get_speechSM, 'questions/Get_speech'),
                                        transitions={'finished': 'if gripper', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'words': 'question'})

            # x:632 y:153
            OperatableStateMachine.add('Stop',
                                        RegexTester(regex=".*(([Nn]o)|([Ss]top)|([Dd]one)).*"),
                                        transitions={'true': 'done', 'false': 'sad'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:633 y:232
            OperatableStateMachine.add('if head',
                                        RegexTester(regex=".*(([Hh]ead)|([Ff]ace)).*"),
                                        transitions={'true': 'show head', 'false': 'Stop'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:633 y:315
            OperatableStateMachine.add('if arm',
                                        RegexTester(regex=".*(([Aa]rm)|([Mm]uscle)).*"),
                                        transitions={'true': 'show arm', 'false': 'if head'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:633 y:387
            OperatableStateMachine.add('if brain',
                                        RegexTester(regex=".*(([Bb]rain)|([Cc]ompute)|([Ll]aptop)).*"),
                                        transitions={'true': 'show brain', 'false': 'if arm'},
                                        autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
                                        remapping={'text': 'question', 'result': 'result'})

            # x:64 y:311
            OperatableStateMachine.add('beep',
                                        SaraSound(sound="ding.wav"),
                                        transitions={'done': 'Get_speech'},
                                        autonomy={'done': Autonomy.Off})

            # x:43 y:149
            OperatableStateMachine.add('ask for questions',
                                        SaraSay(sentence="Just ask your question after the beep sound", emotion=1),
                                        transitions={'done': 'beep'},
                                        autonomy={'done': Autonomy.Off})

            # x:217 y:351
            OperatableStateMachine.add('call other say',
                                        SaraSay(sentence="You can ask me another question if you want", emotion=1),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off})

            # x:429 y:229
            OperatableStateMachine.add('show head',
                                        _sm_show_head_5,
                                        transitions={'done': 'call other say'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:433 y:305
            OperatableStateMachine.add('show arm',
                                        _sm_show_arm_4,
                                        transitions={'done': 'call other say'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:435 y:388
            OperatableStateMachine.add('show brain',
                                        _sm_show_brain_3,
                                        transitions={'done': 'call other say'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:436 y:460
            OperatableStateMachine.add('show base',
                                        _sm_show_base_2,
                                        transitions={'done': 'call other say'},
                                        autonomy={'done': Autonomy.Inherit})

            # x:435 y:532
            OperatableStateMachine.add('show gripper',
                                        _sm_show_gripper_1,
                                        transitions={'done': 'call other say'},
                                        autonomy={'done': Autonomy.Inherit},
                                        remapping={'widthopen': 'widthopen', 'widthclosed': 'widthclosed', 'effort': 'effort'})

            # x:506 y:88
            OperatableStateMachine.add('sad',
                                        PublishUint8(),
                                        transitions={'done': 'Sorry'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'topic': 'topicface', 'data': 'lowmouth'})

            # x:231 y:91
            OperatableStateMachine.add('happy',
                                        PublishUint8(),
                                        transitions={'done': 'ask for questions'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'topic': 'topicface', 'data': 'happy'})



        with _state_machine:
            # x:80 y:66
            OperatableStateMachine.add('start face',
                                        StartFace(),
                                        transitions={'done': 'Greet', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:60 y:291
            OperatableStateMachine.add('questions',
                                        _sm_questions_7,
                                        transitions={'done': 'say goodby', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
                                        remapping={'name': 'name', 'widthopen': 'widthopen', 'widthclosed': 'widthclose', 'effort': 'effort', 'topicface': 'topicface', 'lowmouth': 'lowmouth', 'happy': 'happy'})

            # x:82 y:409
            OperatableStateMachine.add('say goodby',
                                        SaraSayKey(Format=lambda x: "Thank you "+x+" for visiting me. I hope we'll see each others again in the future.", emotion=1),
                                        transitions={'done': 'finished'},
                                        autonomy={'done': Autonomy.Off},
                                        remapping={'sentence': 'name'})

            # x:63 y:182
            OperatableStateMachine.add('Greet',
                                        _sm_greet_6,
                                        transitions={'unavailable': 'failed', 'done': 'questions'},
                                        autonomy={'unavailable': Autonomy.Inherit, 'done': Autonomy.Inherit},
                                        remapping={'topicface': 'topicface', 'happy': 'happy', 'surprise': 'surprise', 'lowmouth': 'lowmouth', 'name': 'name'})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
