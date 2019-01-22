#!/usr/bin/env python

from flexbe_core import EventState, Logger
import rospy
import re

class GetNumberFromText(EventState):
    """
    Give the numerical value of a nominal length

    -- min                  double      the minimum value
    -- max                  double      the maximum value

    ># text                 string      the input text containing the numeric text. eg: "one, two ..."

    #> value                int         the returned value
    #> unit                 string      the unit given
    #> distance_in_meters   int         the distance given in meters

    <= done                 The number has been found
    <= failed               The value is not recognised
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
        unit=""
        for x in self.units:
            regex=".*"+str(x)
            if(re.compile(regex).match(str(userdata.text).lower())):
                unit=str(x)
                userdata.unit=unit

        compteur=0
        for x in self.numbers:
            regex=".*"+str(x)
            if(re.compile(regex).match(str(userdata.text).lower())):
                userdata.value=compteur
                userdata.distance_in_meters = self.calculate_distance_in_meters(compteur,unit)
                return 'done'
            compteur+=1
        userdata.value =0

        return 'failed'

    def calculate_distance_in_meters(self,value,unit):
        if(unit==self.units[0]): #kilometer
            return value*1000
        elif(unit==self.units[1]):#centimeter
            return value/100
        elif(unit==self.units[2]):#meter
            return value
        elif(unit==self.units[3]):#inch
            return value*0.0254
        elif(unit==self.units[4]):#feet
            return value*0.3048
        elif(unit==self.units[5]):#yard
            return value*0.9144
        elif(unit==self.units[6]):#mile
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
