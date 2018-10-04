#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_actionwrapper_attach')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from sara_flexbe_states.sara_say import SaraSay
from sara_flexbe_states.sara_say_key import SaraSayKey
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jul 11 2017
@author: Philippe La Madeleine
'''
class ActionWrapper_AttachSM(Behavior):
	'''
	action wrapper pour attach
	'''


	def __init__(self):
		super(ActionWrapper_AttachSM, self).__init__()
		self.name = 'ActionWrapper_Attach'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
        
        # [/MANUAL_INIT]

		# Behavior comments:

		# O 556 21 
		# Attach|n1- object|n2- where to attach it



	def create(self):
		# x:905 y:379, x:639 y:385, x:230 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'critical_fail'], input_keys=['Action'])
		_state_machine.userdata.Action = ["Atach",'tail','dunky']

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
        
        # [/MANUAL_CREATE]

		# x:30 y:322
		_sm_attach_0 = OperatableStateMachine(outcomes=['finished'])

		with _sm_attach_0:
			# x:52 y:131
			OperatableStateMachine.add('wait',
										WaitState(wait_time=2),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:51 y:46
			OperatableStateMachine.add('cond',
										CheckConditionState(predicate=lambda x: x[1] != ''),
										transitions={'true': 'cond2', 'false': 'say no goal given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:245 y:84
			OperatableStateMachine.add('say no goal given',
										SaraSay(sentence="You didn't told me what to attach", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:44 y:305
			OperatableStateMachine.add('cond2',
										CheckConditionState(predicate=lambda x: x[2] != ''),
										transitions={'true': 'say attach to thing', 'false': 'say no connector given'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'Action'})

			# x:48 y:528
			OperatableStateMachine.add('say no connector given',
										SaraSay(sentence="You didn't told me where to attach it", emotion=1, block=True),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:247 y:309
			OperatableStateMachine.add('say attach to thing',
										SaraSayKey(Format=lambda x: "I'm going to attach that "+x[1]+" to that "+x[2], emotion=1, block=True),
										transitions={'done': 'Attach'},
										autonomy={'done': Autonomy.Off},
										remapping={'sentence': 'Action'})

			# x:462 y:297
			OperatableStateMachine.add('Attach',
										_sm_attach_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
    
    # [/MANUAL_FUNC]
