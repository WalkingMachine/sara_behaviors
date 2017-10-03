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
from flexbe_states.wait_state import WaitState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.regex_tester import RegexTester
from behavior_get_speech.get_speech_sm import Get_speechSM
from sara_flexbe_states.sara_sound import SaraSound
from sara_flexbe_states.unit8_topic_publisher import PublishUint8
from sara_flexbe_states.move_joint import MoveJoint
from sara_flexbe_states.set_gripper_state import SetGripperState
from sara_flexbe_states.sara_move_base import SaraMoveBase
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from sara_flexbe_states.for_loop import ForLoop
from sara_flexbe_states.sara_set_angle import SaraSetAngle
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
		self.add_behavior(Get_speechSM, 'questions/repeat group/Get_speech_2')
		self.add_behavior(Get_speechSM, 'questions/Container/Get_speech')
		self.add_behavior(Get_speechSM, 'Get_speech')
		self.add_behavior(Get_speechSM, 'Get_speech_2')

	# Additional initialization code can be added inside the following tags
	# [MANUAL_INIT]

	# [/MANUAL_INIT]

	# Behavior comments:



	def create(self):
		# x:710 y:437, x:621 y:334
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.name = "you"
		_state_machine.userdata.widthclose = 0
		_state_machine.userdata.widthopen = 250
		_state_machine.userdata.effort = 100
		_state_machine.userdata.topicface = "/control_emo"
		_state_machine.userdata.happy = 1
		_state_machine.userdata.wink = 6
		_state_machine.userdata.surprise = 5
		_state_machine.userdata.lowmouth = 3
		_state_machine.userdata.crazy = 7
		_state_machine.userdata.index = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:925 y:24
		_sm_container_0 = OperatableStateMachine(outcomes=['done'])

		with _sm_container_0:
			# x:73 y:59
			OperatableStateMachine.add('ask destination',
									   SaraSay(sentence="Ok, where do you want me to go", emotion=1),
									   transitions={'done': 'beep'},
									   autonomy={'done': Autonomy.Off})

			# x:85 y:154
			OperatableStateMachine.add('beep',
									   SaraSound(sound="ding.wav"),
									   transitions={'done': 'Get_speech'},
									   autonomy={'done': Autonomy.Off})

			# x:68 y:258
			OperatableStateMachine.add('Get_speech',
									   self.use_behavior(Get_speechSM, 'questions/Container/Get_speech'),
									   transitions={'finished': 'room', 'failed': 'room'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'destination'})

			# x:774 y:176
			OperatableStateMachine.add('move',
									   SaraMoveBase(),
									   transitions={'arrived': 'arived', 'failed': 'sorry'},
									   autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
									   remapping={'pose': 'pose'})

			# x:278 y:519
			OperatableStateMachine.add('room',
									   RegexTester(regex=".*([Rr]oom)|([Bb]ad).*"),
									   transitions={'true': 'say room', 'false': 'kitchen'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'destination', 'result': 'result'})

			# x:533 y:532
			OperatableStateMachine.add('gen room',
									   GenPoseEuler(x=4.2, y=4.2, z=0, roll=0, pitch=0, yaw=1.5),
									   transitions={'done': 'move', 'failed': 'sorry'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
									   remapping={'pose': 'pose'})

			# x:791 y:546
			OperatableStateMachine.add('sorry',
									   SaraSay(sentence="Sorry, I think I'm stuck", emotion=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})

			# x:276 y:395
			OperatableStateMachine.add('kitchen',
									   RegexTester(regex=".*([Tt]able)|([Kk]itchen).*"),
									   transitions={'true': 'say kitchen', 'false': 'door'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'destination', 'result': 'result'})

			# x:281 y:275
			OperatableStateMachine.add('door',
									   RegexTester(regex=".*([Dd]oor)|([Bb]ack)|([Hh]ere).*"),
									   transitions={'true': 'say door', 'false': 'say'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'destination', 'result': 'result'})

			# x:545 y:272
			OperatableStateMachine.add('gen door',
									   GenPoseEuler(x=0.6, y=0, z=0, roll=0, pitch=0, yaw=3.14),
									   transitions={'done': 'move', 'failed': 'sorry'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
									   remapping={'pose': 'pose'})

			# x:290 y:23
			OperatableStateMachine.add('say',
									   SaraSay(sentence="Sorry, I don't know this place.", emotion=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})

			# x:411 y:393
			OperatableStateMachine.add('say kitchen',
									   SaraSay(sentence="Okay, I'm going to the kitchen", emotion=1),
									   transitions={'done': 'gen kitchen'},
									   autonomy={'done': Autonomy.Off})

			# x:423 y:521
			OperatableStateMachine.add('say room',
									   SaraSay(sentence="Okay, I'm going to my room", emotion=1),
									   transitions={'done': 'gen room'},
									   autonomy={'done': Autonomy.Off})

			# x:422 y:270
			OperatableStateMachine.add('say door',
									   SaraSay(sentence="Okay, I'm coming back to the door.", emotion=1),
									   transitions={'done': 'gen door'},
									   autonomy={'done': Autonomy.Off})

			# x:542 y:381
			OperatableStateMachine.add('gen kitchen',
									   GenPoseEuler(x=3.8, y=0.5, z=0, roll=0, pitch=0, yaw=-1.5),
									   transitions={'done': 'move', 'failed': 'sorry'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
									   remapping={'pose': 'pose'})

			# x:795 y:76
			OperatableStateMachine.add('arived',
									   SaraSay(sentence="Here I am.", emotion=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})


		# x:124 y:375, x:561 y:240
		_sm_repeat_group_1 = OperatableStateMachine(outcomes=['failed', 'finished'])

		with _sm_repeat_group_1:
			# x:61 y:47
			OperatableStateMachine.add('say1',
									   SaraSay(sentence="Say anything and I'll repeat after you.", emotion=1),
									   transitions={'done': 'Get_speech_2'},
									   autonomy={'done': Autonomy.Off})

			# x:255 y:126
			OperatableStateMachine.add('say',
									   SaraSayKey(Format=lambda x: x, emotion=1),
									   transitions={'done': 'Get_speech_2'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'sentence': 'words'})

			# x:393 y:227
			OperatableStateMachine.add('test',
									   RegexTester(regex=".*[Ss]top.*"),
									   transitions={'true': 'finished', 'false': 'say'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'words', 'result': 'result'})

			# x:56 y:198
			OperatableStateMachine.add('Get_speech_2',
									   self.use_behavior(Get_speechSM, 'questions/repeat group/Get_speech_2'),
									   transitions={'finished': 'test', 'failed': 'failed'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'words'})


		# x:379 y:592
		_sm_show_gripper_2 = OperatableStateMachine(outcomes=['done'], input_keys=['widthopen', 'widthclosed', 'effort'])

		with _sm_show_gripper_2:
			# x:30 y:40
			OperatableStateMachine.add('respond gripper',
									   SaraSay(sentence="My gripper is build by Robotiq and allows me to pick up things.", emotion=1),
									   transitions={'done': 'opp'},
									   autonomy={'done': Autonomy.Off})

			# x:38 y:236
			OperatableStateMachine.add('close',
									   SetGripperState(),
									   transitions={'done': 'say catch'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'width': 'widthclosed', 'effort': 'effort'})

			# x:52 y:479
			OperatableStateMachine.add('open',
									   SetGripperState(),
									   transitions={'done': 'lower'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'width': 'widthopen', 'effort': 'effort'})

			# x:63 y:389
			OperatableStateMachine.add('say catch',
									   SaraSay(sentence="I am an excellent catch", emotion=1),
									   transitions={'done': 'open'},
									   autonomy={'done': Autonomy.Off})

			# x:66 y:127
			OperatableStateMachine.add('show',
									   MoveJoint(pose_name="ShowGripper"),
									   transitions={'done': 'close', 'failed': 'close'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:116 y:568
			OperatableStateMachine.add('lower',
									   MoveJoint(pose_name="IdlePose"),
									   transitions={'done': 'done', 'failed': 'done'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:234 y:82
			OperatableStateMachine.add('opp',
									   SetGripperState(),
									   transitions={'done': 'show'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'width': 'widthopen', 'effort': 'effort'})


		# x:30 y:325
		_sm_show_base_3 = OperatableStateMachine(outcomes=['done'])

		with _sm_show_base_3:
			# x:30 y:40
			OperatableStateMachine.add('respond base',
									   SaraSay(sentence="My base is what allows me to move. I can go in any direction thanks to my mecanum wheels and motor controllers.", emotion=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})


		# x:30 y:325
		_sm_show_brain_4 = OperatableStateMachine(outcomes=['done'])

		with _sm_show_brain_4:
			# x:30 y:40
			OperatableStateMachine.add('say brain',
									   SaraSay(sentence="My brain is located inside my laptop. You can call me a no brainer.", emotion=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})


		# x:102 y:523
		_sm_show_arm_5 = OperatableStateMachine(outcomes=['done'], input_keys=['topicface', 'lowmouth', 'happy'])

		with _sm_show_arm_5:
			# x:75 y:37
			OperatableStateMachine.add('say arm',
									   SaraSay(sentence="My arm is custom made from 3d printed titanium and use Kinova high precision harmonic drives to move. Watch my moves!", emotion=1),
									   transitions={'done': 'show'},
									   autonomy={'done': Autonomy.Off})

			# x:41 y:338
			OperatableStateMachine.add('move to idle',
									   MoveJoint(pose_name="IdlePose"),
									   transitions={'done': 'done', 'failed': 'sad'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:60 y:239
			OperatableStateMachine.add('say cap',
									   SaraSay(sentence="With these, I can lift up to 2 pounds.", emotion=1),
									   transitions={'done': 'move to idle'},
									   autonomy={'done': Autonomy.Off})

			# x:57 y:134
			OperatableStateMachine.add('show',
									   MoveJoint(pose_name="ShowGripper"),
									   transitions={'done': 'say cap', 'failed': 'sad'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:285 y:269
			OperatableStateMachine.add('sayerror',
									   SaraSay(sentence="well, It does that from time to time. Anyway let's move on.", emotion=1),
									   transitions={'done': 'happy'},
									   autonomy={'done': Autonomy.Off})

			# x:275 y:129
			OperatableStateMachine.add('sad',
									   PublishUint8(),
									   transitions={'done': 'sayerror'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'lowmouth'})

			# x:224 y:372
			OperatableStateMachine.add('happy',
									   PublishUint8(),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'happy'})


		# x:141 y:455
		_sm_show_head_6 = OperatableStateMachine(outcomes=['done'], input_keys=['crazy', 'topicface', 'happy'])

		with _sm_show_head_6:
			# x:30 y:40
			OperatableStateMachine.add('say head',
									   SaraSay(sentence="My head is composed of my eyes, which are made of a 3d camera. I also have 80 LED that allows me to simulate human emotions.", emotion=1),
									   transitions={'done': 'crazy'},
									   autonomy={'done': Autonomy.Off})

			# x:105 y:144
			OperatableStateMachine.add('crazy',
									   PublishUint8(),
									   transitions={'done': 'say hard'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'crazy'})

			# x:148 y:232
			OperatableStateMachine.add('say hard',
									   SaraSay(sentence="Human emotion are so complicated.", emotion=1),
									   transitions={'done': 'normal'},
									   autonomy={'done': Autonomy.Off})

			# x:177 y:343
			OperatableStateMachine.add('normal',
									   PublishUint8(),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'happy'})


		# x:479 y:319, x:481 y:479
		_sm_get_name_7 = OperatableStateMachine(outcomes=['unavailable', 'true'], input_keys=['topicface', 'surprise', 'lowmouth', 'happy'], output_keys=['name'])

		with _sm_get_name_7:
			# x:56 y:40
			OperatableStateMachine.add('ask for name',
									   SaraSay(sentence="Just say your name after the beep sound", emotion=1),
									   transitions={'done': 'wait1'},
									   autonomy={'done': Autonomy.Off})

			# x:41 y:343
			OperatableStateMachine.add('say name',
									   SaraSayKey(Format=lambda x: "Did you say your name was "+x+"?", emotion=1),
									   transitions={'done': 'wait4'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'sentence': 'name'})

			# x:256 y:467
			OperatableStateMachine.add('check responce',
									   RegexTester(regex=".*(([Oo]k)|([Yy]es)|([Yy]ea)|([Ss]ure)|([Ii]ndeed)).*"),
									   transitions={'true': 'true', 'false': 'low'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'validation', 'result': 'result'})

			# x:45 y:428
			OperatableStateMachine.add('wait4',
									   WaitState(wait_time=0.1),
									   transitions={'done': 'Get_speech_2'},
									   autonomy={'done': Autonomy.Off})

			# x:25 y:242
			OperatableStateMachine.add('Get_speech',
									   self.use_behavior(Get_speechSM, 'Greet/Get name/Get_speech'),
									   transitions={'finished': 'say name', 'failed': 'unavailable'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'name'})

			# x:28 y:513
			OperatableStateMachine.add('Get_speech_2',
									   self.use_behavior(Get_speechSM, 'Greet/Get name/Get_speech_2'),
									   transitions={'finished': 'check responce', 'failed': 'unavailable'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'validation'})

			# x:47 y:172
			OperatableStateMachine.add('play pign',
									   SaraSound(sound="ding.wav"),
									   transitions={'done': 'Get_speech'},
									   autonomy={'done': Autonomy.Off})

			# x:232 y:260
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

			# x:214 y:170
			OperatableStateMachine.add('happy',
									   PublishUint8(),
									   transitions={'done': 'wait1'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'happy'})

			# x:60 y:98
			OperatableStateMachine.add('wait1',
									   WaitState(wait_time=0.1),
									   transitions={'done': 'play pign'},
									   autonomy={'done': Autonomy.Off})


		# x:930 y:175, x:217 y:461
		_sm_questions_8 = OperatableStateMachine(outcomes=['done', 'failed'], input_keys=['name', 'widthopen', 'widthclosed', 'effort', 'topicface', 'lowmouth', 'happy', 'crazy'])

		with _sm_questions_8:
			# x:55 y:43
			OperatableStateMachine.add('say question',
									   SaraSayKey(Format=lambda x: "Now "+x+". You can ask me about my head, arm, hand, base, wheel and brain.", emotion=1),
									   transitions={'done': 'ask for questions'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'sentence': 'name'})

			# x:631 y:530
			OperatableStateMachine.add('if gripper',
									   RegexTester(regex=".*((gripper)|(hand)|(claw)).*"),
									   transitions={'true': 'show gripper', 'false': 'if base'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:635 y:457
			OperatableStateMachine.add('if base',
									   RegexTester(regex=".*((base)|(wheel)|(bottom)|(legs)|(move)).*"),
									   transitions={'true': 'show base', 'false': 'if brain'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:382 y:88
			OperatableStateMachine.add('Sorry',
									   SaraSay(sentence="sorry I did not understand", emotion=1),
									   transitions={'done': 'ask for questions'},
									   autonomy={'done': Autonomy.Off})

			# x:42 y:548
			OperatableStateMachine.add('Get_speech',
									   self.use_behavior(Get_speechSM, 'questions/Get_speech'),
									   transitions={'finished': 'nav', 'failed': 'failed'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'question'})

			# x:632 y:84
			OperatableStateMachine.add('Stop',
									   RegexTester(regex=".*((no)|(stop)|(done)|(over)|(thank)|(enough)).*"),
									   transitions={'true': 'done', 'false': 'sad'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:633 y:232
			OperatableStateMachine.add('if head',
									   RegexTester(regex=".*((head)|(face)).*"),
									   transitions={'true': 'show head', 'false': 'repeat'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:633 y:315
			OperatableStateMachine.add('if arm',
									   RegexTester(regex=".*((arm)|(muscle)).*"),
									   transitions={'true': 'show arm', 'false': 'if head'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:633 y:387
			OperatableStateMachine.add('if brain',
									   RegexTester(regex=".*((brain)|(compute)|(laptop)).*"),
									   transitions={'true': 'show brain', 'false': 'if arm'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:44 y:397
			OperatableStateMachine.add('beep',
									   SaraSound(sound="ding.wav"),
									   transitions={'done': 'Get_speech'},
									   autonomy={'done': Autonomy.Off})

			# x:43 y:121
			OperatableStateMachine.add('ask for questions',
									   SaraSay(sentence="Just ask your question after the beep sound", emotion=1),
									   transitions={'done': 'happy'},
									   autonomy={'done': Autonomy.Off})

			# x:217 y:351
			OperatableStateMachine.add('call other say',
									   SaraSay(sentence="You can ask me another question if you want", emotion=1),
									   transitions={'done': 'ask for questions'},
									   autonomy={'done': Autonomy.Off})

			# x:429 y:229
			OperatableStateMachine.add('show head',
									   _sm_show_head_6,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit},
									   remapping={'crazy': 'crazy', 'topicface': 'topicface', 'happy': 'happy'})

			# x:433 y:305
			OperatableStateMachine.add('show arm',
									   _sm_show_arm_5,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit},
									   remapping={'topicface': 'topicface', 'lowmouth': 'lowmouth', 'happy': 'happy'})

			# x:435 y:388
			OperatableStateMachine.add('show brain',
									   _sm_show_brain_4,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit})

			# x:436 y:460
			OperatableStateMachine.add('show base',
									   _sm_show_base_3,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit})

			# x:435 y:532
			OperatableStateMachine.add('show gripper',
									   _sm_show_gripper_2,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit},
									   remapping={'widthopen': 'widthopen', 'widthclosed': 'widthclosed', 'effort': 'effort'})

			# x:506 y:88
			OperatableStateMachine.add('sad',
									   PublishUint8(),
									   transitions={'done': 'Sorry'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'lowmouth'})

			# x:55 y:200
			OperatableStateMachine.add('happy',
									   PublishUint8(),
									   transitions={'done': 'wait1'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'happy'})

			# x:634 y:165
			OperatableStateMachine.add('repeat',
									   RegexTester(regex=".*repeat.*me.*"),
									   transitions={'true': 'repeat group', 'false': 'Stop'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:426 y:159
			OperatableStateMachine.add('repeat group',
									   _sm_repeat_group_1,
									   transitions={'failed': 'call other say', 'finished': 'call other say'},
									   autonomy={'failed': Autonomy.Inherit, 'finished': Autonomy.Inherit})

			# x:48 y:292
			OperatableStateMachine.add('wait1',
									   WaitState(wait_time=0.1),
									   transitions={'done': 'beep'},
									   autonomy={'done': Autonomy.Off})

			# x:632 y:612
			OperatableStateMachine.add('nav',
									   RegexTester(regex=".*((navigation)|(go)|(walk)|(roll)|(travel)).*"),
									   transitions={'true': 'Container', 'false': 'if gripper'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'question', 'result': 'result'})

			# x:437 y:607
			OperatableStateMachine.add('Container',
									   _sm_container_0,
									   transitions={'done': 'call other say'},
									   autonomy={'done': Autonomy.Inherit})


		# x:294 y:283, x:283 y:499
		_sm_greet_9 = OperatableStateMachine(outcomes=['unavailable', 'done'], input_keys=['topicface', 'happy', 'surprise', 'lowmouth'], output_keys=['name'])

		with _sm_greet_9:
			# x:48 y:40
			OperatableStateMachine.add('wait',
									   WaitState(wait_time=1),
									   transitions={'done': 'face happy'},
									   autonomy={'done': Autonomy.Off})

			# x:47 y:114
			OperatableStateMachine.add('say hello',
									   SaraSay(sentence="Hi, my name is sarah. I am a human assistant robot made by the student club Walking Machine of ETS.", emotion=1),
									   transitions={'done': 'wait2'},
									   autonomy={'done': Autonomy.Off})

			# x:46 y:183
			OperatableStateMachine.add('wait2',
									   WaitState(wait_time=0.1),
									   transitions={'done': 'call name'},
									   autonomy={'done': Autonomy.Off})

			# x:50 y:492
			OperatableStateMachine.add('wait4',
									   WaitState(wait_time=1),
									   transitions={'done': 'done'},
									   autonomy={'done': Autonomy.Off})

			# x:32 y:336
			OperatableStateMachine.add('Get name',
									   _sm_get_name_7,
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
									   SaraSay(sentence="Could you tell me your name please?", emotion=1),
									   transitions={'done': 'Get name'},
									   autonomy={'done': Autonomy.Off})

			# x:196 y:114
			OperatableStateMachine.add('face happy',
									   PublishUint8(),
									   transitions={'done': 'say hello'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'topic': 'topicface', 'data': 'happy'})



		with _state_machine:
			# x:74 y:26
			OperatableStateMachine.add('start face',
									   StartFace(),
									   transitions={'done': 'set head angle', 'failed': 'set head angle'},
									   autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:45 y:494
			OperatableStateMachine.add('say goodby',
									   SaraSayKey(Format=lambda x: "Thank you "+x+" for visiting me. I hope we'll see each others again in the future.", emotion=1),
									   transitions={'done': 'goodbye'},
									   autonomy={'done': Autonomy.Off},
									   remapping={'sentence': 'name'})

			# x:43 y:301
			OperatableStateMachine.add('Greet',
									   _sm_greet_9,
									   transitions={'unavailable': 'failed', 'done': 'questions'},
									   autonomy={'unavailable': Autonomy.Inherit, 'done': Autonomy.Inherit},
									   remapping={'topicface': 'topicface', 'happy': 'happy', 'surprise': 'surprise', 'lowmouth': 'lowmouth', 'name': 'name'})

			# x:30 y:386
			OperatableStateMachine.add('questions',
									   _sm_questions_8,
									   transitions={'done': 'say goodby', 'failed': 'failed'},
									   autonomy={'done': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'name': 'name', 'widthopen': 'widthopen', 'widthclosed': 'widthclose', 'effort': 'effort', 'topicface': 'topicface', 'lowmouth': 'lowmouth', 'happy': 'happy', 'crazy': 'crazy'})

			# x:416 y:610
			OperatableStateMachine.add('bye',
									   RegexTester(regex=".*(([Gg]ood)|([Bb]ye)|([Nn]ight)|([Bb]ite)|([Ss]ee)).*"),
									   transitions={'true': 'for 3', 'false': 'Get_speech_2'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'bye', 'result': 'result'})

			# x:45 y:581
			OperatableStateMachine.add('goodbye',
									   SaraSay(sentence="goodbye", emotion=1),
									   transitions={'done': 'Get_speech'},
									   autonomy={'done': Autonomy.Off})

			# x:324 y:541
			OperatableStateMachine.add('say',
									   SaraSay(sentence="bye", emotion=1),
									   transitions={'done': 'Get_speech'},
									   autonomy={'done': Autonomy.Off})

			# x:439 y:524
			OperatableStateMachine.add('for 3',
									   ForLoop(repeat=2),
									   transitions={'do': 'say', 'end': 'sayend'},
									   autonomy={'do': Autonomy.Off, 'end': Autonomy.Off},
									   remapping={'index': 'index'})

			# x:438 y:450
			OperatableStateMachine.add('sayend',
									   SaraSay(sentence="Ok, that's enough. Please leave now.", emotion=1),
									   transitions={'done': 'Get_speech_2'},
									   autonomy={'done': Autonomy.Off})

			# x:149 y:583
			OperatableStateMachine.add('Get_speech',
									   self.use_behavior(Get_speechSM, 'Get_speech'),
									   transitions={'finished': 'bye', 'failed': 'Get_speech_2'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'bye'})

			# x:59 y:228
			OperatableStateMachine.add('get hello',
									   RegexTester(regex=".*(([Hh]ello)|([Hh]i)|([Dd]ay)|([Ss]ara)).*"),
									   transitions={'true': 'Greet', 'false': 'Get_speech_2'},
									   autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
									   remapping={'text': 'hello', 'result': 'result'})

			# x:52 y:115
			OperatableStateMachine.add('Get_speech_2',
									   self.use_behavior(Get_speechSM, 'Get_speech_2'),
									   transitions={'finished': 'get hello', 'failed': 'Get_speech_2'},
									   autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
									   remapping={'words': 'hello'})

			# x:268 y:53
			OperatableStateMachine.add('set head angle',
									   SaraSetAngle(angle=0),
									   transitions={'done': 'Get_speech_2'},
									   autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
