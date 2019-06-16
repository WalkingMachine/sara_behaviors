#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger
import copy

import math
'''
Created on 18.03.2019

@author: Philippe La Madeleine
'''


class FilterKey(EventState):
    '''
                            ALlows the user to filter data using a lambda function and a custom selection of input_keys.

    -- filter  function	    The lambda function applied to all elements of the list.
                            Here, x[0] is always referring to each individual elements in the the list.
                            ex: "lambda x: x[0].ID == x[1]"

    -- input_keys           Input to the filter function. The first element shall allays be the input_list.

    ># input_list  list		The first element of the input_keys. Contain the list to filter.

    #> output_list list		The result of the filter.

    <= not_empty			Indicates completion of the filtration with a non-empty list.
    <= empty                Indicates completion of the filtration with an empty list.
    '''

    def __init__(self, filter_function, input_keys=["input_list"]):
        '''
        Constructor
        '''
        super(FilterKey, self).__init__(outcomes=['not_empty', 'empty'],
                                               input_keys=input_keys,
                                               output_keys=['output_list'])

        self.filter_function = filter_function
        self.input_keys = input_keys

    def execute(self, userdata):
        '''Execute this state'''

        output = self.filterbyvalue(userdata, self.filter_function)
        userdata.output_list = output

        Logger.loginfo(str(userdata.input_list))

        if len(output) > 0:
            return 'not_empty'
        else:
            return 'empty'


    def filterbyvalue(self, userdata, filter_function):

        output = []

        li = list(map(lambda key: userdata[key], list(self.input_keys)))
        print("x = "+str(li))

        for el in li[0]:
            x = copy.copy(li)

            x[0] = el
            if filter_function(x):
                output.append(el)
        return output
