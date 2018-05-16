#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 9.05.2018

@author: Philippe La Madeleine
'''


class BinaryCalculationState(EventState):
    '''
	Implements a state that can perform a binary calculation based on userdata.
	calculation is a function which takes exactly two parameter, X and Y from userdata,
	and its return value is stored in output_value after leaving the state. e.g. "X+Y" will return the sum of X and Y into the output Z.
	
	-- calculation  string	The function that performs the desired calculation.
								It could be a private function (self.foo) manually defined in a behavior's source code
								or a lambda function (e.g., "f = x, y: x^2 +y", where x will be the input_value).

	># X  object		Input to the calculation function.
	># Y  object		Input to the calculation function.

	#> Z object		The result of the calculation.

	<= done						Indicates completion of the calculation.

	'''

    def __init__(self, calculation):
        '''
		Constructor
		'''
        super(BinaryCalculationState, self).__init__(outcomes=['done'],
                                                     input_keys=['X', 'Y'],
                                                     output_keys=['Z'])

        self._calculation = calculation
        self._calculation_result = None

    def execute(self, userdata):
        '''Execute this state'''

        userdata.Z = self._calculation_result

        # nothing to check
        return 'done'

    def on_enter(self, userdata):

        if self._calculation is not None:
            try:
                X = userdata.X
                Y = userdata.Y
                Z = 0
                self._calculation_result = eval(self._calculation)
            except Exception as e:
                Logger.logwarn('Failed to execute calculation function!\n%s' % str(e))
        else:
            Logger.logwarn('Passed no calculation!')
