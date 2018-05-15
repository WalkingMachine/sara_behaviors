#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_scenario_security_check')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from sara_flexbe_states.SetKey import SetKey
from sara_flexbe_states.sara_sound import SaraSound
from sara_flexbe_states.pose_gen_euler import GenPoseEuler
from behavior_action_move.action_move_sm import Action_MoveSM
from sara_flexbe_states.continue_button import ContinueButton
from sara_flexbe_states.sara_say import SaraSay
from behavior_action_pass_door.action_pass_door_sm import Action_Pass_DoorSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on 12 mai 2018
@author: Veronica Romero
'''
class Scenario_Security_CheckSM(Behavior):
	'''
	englobe le scenario du test de securite.
	'''


	def __init__(self):
		super(Scenario_Security_CheckSM, self).__init__()
		self.name = 'Scenario_Security_Check'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Action_MoveSM, 'Move to test zone')
		self.add_behavior(Action_Pass_DoorSM, 'Action_Pass_Door')
		self.add_behavior(Action_Pass_DoorSM, 'Action_Pass_Door_2')

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
			# x:49 y:34
			OperatableStateMachine.add('set not relative',
										SetKey(Value=False),
										transitions={'done': 'gen door pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'Key': 'relative'})

			# x:37 y:612
			OperatableStateMachine.add('Failed',
										SaraSound(sound="error.wav"),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:395 y:549
			OperatableStateMachine.add('Waiting',
										SaraSound(sound="to_be_continued.wav"),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:706 y:445
			OperatableStateMachine.add('Gen test zone exit',
										GenPoseEuler(x=2.26782121774, y=-6.1888976361, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Action_Pass_Door_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:28 y:453
			OperatableStateMachine.add('Move to test zone',
										self.use_behavior(Action_MoveSM, 'Move to test zone'),
										transitions={'finished': 'say ready', 'failed': 'Failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'relative': 'relative'})

			# x:189 y:9
			OperatableStateMachine.add('Bouton to start',
										ContinueButton(),
										transitions={'true': 'set not relative', 'false': 'Bouton to start'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:250 y:448
			OperatableStateMachine.add('say ready',
										SaraSay(sentence="I'm ready for my safety check. Press the continue button on my back when you are done.", emotion=1, block=True),
										transitions={'done': 'Bouton continuer'},
										autonomy={'done': Autonomy.Off})

			# x:32 y:332
			OperatableStateMachine.add('Gen test zone position',
										GenPoseEuler(x=1.27, y=-5.7165979361, z=0, roll=0, pitch=0, yaw=90),
										transitions={'done': 'Move to test zone'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:36 y:221
			OperatableStateMachine.add('Action_Pass_Door',
										self.use_behavior(Action_Pass_DoorSM, 'Action_Pass_Door'),
										transitions={'Done': 'Gen test zone position', 'Fail': 'Action_Pass_Door'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'DoorPose1'})

			# x:53 y:122
			OperatableStateMachine.add('gen door pose',
										GenPoseEuler(x=-0.1, y=-5.68, z=0, roll=0, pitch=0, yaw=0),
										transitions={'done': 'Action_Pass_Door'},
										autonomy={'done': Autonomy.Off},
										remapping={'pose': 'DoorPose1'})

			# x:410 y:453
			OperatableStateMachine.add('Bouton continuer',
										ContinueButton(),
										transitions={'true': 'say bye', 'false': 'Waiting'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off})

			# x:987 y:420
			OperatableStateMachine.add('Action_Pass_Door_2',
										self.use_behavior(Action_Pass_DoorSM, 'Action_Pass_Door_2'),
										transitions={'Done': 'finished', 'Fail': 'Action_Pass_Door_2'},
										autonomy={'Done': Autonomy.Inherit, 'Fail': Autonomy.Inherit},
										remapping={'DoorPose1': 'pose'})

			# x:583 y:446
			OperatableStateMachine.add('say bye',
										SaraSay(sentence="Thank you, See you later.", emotion=1, block=True),
										transitions={'done': 'Gen test zone exit'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
