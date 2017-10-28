#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re

class GetNumberFromText(EventState):
    """
    genere une valeur numerique a partir d'un nombre nominal.

    ### parameters
    -- min
    -- max

    ### InputKey
    ># text

    ### OutputKey
    #> value
    #> unit

    <= done
    <= failed
    """

    def __init__(self, min, max):
        """Constructor"""

        super(GetNumberFromText, self).__init__(outcomes = ['done','failed'], input_keys = ['text'], output_keys = ['value','unit'])
        self.min =min
        self.max=max

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""
        numbers= ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"]
        units=['kilometer','centimeter','meter','inch','feet','yard','mile']

        userdata.unit="meter"
        for x in units:
            regex=".*"+str(x)
            if(re.compile(regex).match(str(userdata.text).lower())):
                userdata.unit=str(x)

        compteur=0
        for x in numbers:
            regex=".*"+str(x)
            if(re.compile(regex).match(str(userdata.text).lower())):
                userdata.value=compteur
                return 'done'
            compteur+=1
        userdata.value =0

        return 'failed'
