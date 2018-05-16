#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_action_guiding_person')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from behavior_get_operator.get_operator_sm import Get_operatorSM
from sara_flexbe_states.sara_say import SaraSay
from flexbe_navigation_states.move_base_state import MoveBaseState
from sara_flexbe_states.GetRosParam import GetRosParam
from sara_flexbe_states.Get_Entity_By_ID import GetEntityByID
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat May 12 2018
@author: Huynh-Anh Le
'''
class Action_Guiding_PersonSM(Behavior):
	'''
	Sara will guide someone
	'''


	def __init__(self):
		super(Action_Guiding_PersonSM, self).__init__()
		self.name = 'Action_Guiding_Person'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Get_operatorSM, 'Get_operator')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 218 87 
		# trouve la personne et sassure quelle reste proche

		# O 318 259 
		# si elle disparait, on la retrouve!!

		# O 278 118 /deplacement et verification de presence/verifie presence
		# on trouve lID de operateur 



	def create(self):
		# x:746 y:544, x:65 y:361
		_state_machine = OperatableStateMachine(outcomes=['finished', 'not found'], input_keys=['Position'])
		_state_machine.userdata.Position = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365
		_sm_verifie_presence_0 = OperatableStateMachine(outcomes=['not found'])

		with _sm_verifie_presence_0:
			# x:90 y:107
			OperatableStateMachine.add('getID',
										GetRosParam(ParamName="OperatorID"),
										transitions={'done': 'getOperator', 'failed': 'not found'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'Value': 'ID'})

			# x:297 y:176
			OperatableStateMachine.add('getOperator',
										GetEntityByID(),
										transitions={'found': 'getID', 'not_found': 'not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ID': 'ID', 'Entity': 'Operator'})


		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_deplacement_et_verification_de_presence_1 = ConcurrencyContainer(outcomes=['arrived', 'failed'], input_keys=['Position'], conditions=[
										('arrived', [('sara_move', 'arrived')]),
										('failed', [('sara_move', 'failed')]),
										('failed', [('verifie presence', 'not found')])
										])

		with _sm_deplacement_et_verification_de_presence_1:
			# x:30 y:101
			OperatableStateMachine.add('sara_move',
										MoveBaseState(),
										transitions={'arrived': 'arrived', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'Position'})

			# x:255 y:90
			OperatableStateMachine.add('verifie presence',
										_sm_verifie_presence_0,
										transitions={'not found': 'failed'},
										autonomy={'not found': Autonomy.Inherit})



		with _state_machine:
			# x:55 y:57
			OperatableStateMachine.add('Get_operator',
										self.use_behavior(Get_operatorSM, 'Get_operator'),
										transitions={'Found': 'foundyou!', 'NotFound': 'not found'},
										autonomy={'Found': Autonomy.Inherit, 'NotFound': Autonomy.Inherit},
										remapping={'Operator': 'Operator'})

			# x:208 y:184
			OperatableStateMachine.add('foundyou!',
										SaraSay(sentence="Operator, please follow me", emotion=1, block=True),
										transitions={'done': 'deplacement et verification de presence'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:500
			OperatableStateMachine.add('destinationreached',
										SaraSay(sentence="We have reached our destination", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:247 y:319
			OperatableStateMachine.add('deplacement et verification de presence',
										_sm_deplacement_et_verification_de_presence_1,
										transitions={'arrived': 'destinationreached', 'failed': 'lostyou'},
										autonomy={'arrived': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'Position': 'Position'})

			# x:599 y:180
			OperatableStateMachine.add('lostyou',
										SaraSay(sentence="I lost you, please stay where you are", emotion=1, block=True),
										transitions={'done': 'Get_operator'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
