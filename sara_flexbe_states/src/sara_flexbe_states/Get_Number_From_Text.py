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
    #> distance_in_meters

    <= done
    <= failed
    """
    numbers= ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"]
    units=['kilometer','centimeter','meter','inch','feet','yard','mile']

    def __init__(self, min, max):
        """Constructor"""

        super(GetNumberFromText, self).__init__(outcomes = ['done','failed'], input_keys = ['text'], output_keys = ['value','unit','distance_in_meters'])
        self.min=min
        self.max=max

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""


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
                userdata.distance_in_meters = calculate_distance_in_meters(userdata.value,userdata.unit)
                return 'done'
            compteur+=1
        userdata.value =0

        return 'failed'

    def calculate_distance_in_meters(value,unit):
        if(unit==units[0]): #kilometer
            return value*1000
        elif(unit==units[1]):#centimeter
            return value/100
        elif(unit==units[2]):#meter
            return value
        elif(unit==units[3]):#inch
            return value*0.0254
        elif(unit==units[4]):#feet
            return value*0.3048
        elif(unit==units[5]):#yard
            return value*0.9144
        elif(unit==units[6]):#mile
            return value*1609.344
        else:
            print("Could understand the unit")
            return -1
        """
    1 inch = 0.0254 meters
    1 hand = 0.1016 meters
    1 link = 0.201168 meters
    1 foot = 0.3048 meters
    1 yard = 0.9144 meters
    1 fathom = 1.8288002 meters
    1 rod/pole/perch = 5.0291995 meters
    1 chain = 20.1167981 meters
    1 cable = 185.3190 meters
    1 furlong = 201.1708 meters
    1 mile = 1,609.344 meters
    1 nautical mile = 1,852 meters
    """
