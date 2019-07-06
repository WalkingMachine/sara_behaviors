#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

'''
Created on 6.07.2019

@author: Huynh-Anh Le
'''


class TourGuide(EventState):
    '''
    Implements a state will give the sequence to get to the object needed.
    state will return the sequence to travel to the object's room.


    ># startingRoom string	informationPoint's room. Must be "office", "living room", "kitchen" or "bedroom"

    ># endingRoom string	where the object should be found. Must be "office", "living room", "kitchen" or "bedroom"

    ># dictRoomToRoom  dict	dictionnary of the directions from room to room

    ># object  string		name of the object that needs to be located

    #> sequence list	     	the ending combined sequence

    <= done			The sequence as been generated.

    '''


    def __init__(self):
        '''
        Constructor
        '''

        super(TourGuide, self).__init__(outcomes=['done'],
                                        input_keys=['object', 'startingRoom', 'endingRoom'],
                                        output_keys=['sequence'])

        self._calculation_result = None
	self.dictdirect = {"officekitchen": [["say", "The _object is in the kitchen"],["wait", 0.5],["say","you can get to the kitchen by going to the Living Room behind me and then opening the door to your right."],  ["wait", 0.5],["say", "Once you are there the object will be left"],["wait", 0.5],["say", "let me show you"],["move", "office-living room"],["wait", 1.0],["say", "We are entering the living room. The couch is on my right and The Coffee Table is in front of me"],["move", "kitchen"]],"bedroomkitchen": [["say", "The _object is in the kitchen"],["wait", 0.5],["say", "you can get to the kitchen by the door to my right."],["wait", 0.5],["say", "Once you are there the object will be left."],["wait", 0.5],["say", "let me show you"],["passdoor", "bedroom-kitchen"],["say", "We are entering the kitchen. The fridge is on my left and The trash bin is in front of me"],["move", "kitchen"]],"living roomkitchen": [["say", "The _object is in the kitchen"],["wait", 0.5],["say", "you can get to the kitchen by the door to my left."],["wait", 0.5],["say", "let me show you"],["move", "living room-kitchen"],["say", "We are entering the kitchen. The fridge is on my left and The kitchen table is on my right"],["move", "kitchen"]],"kitchenkitchen": [["say", "The _object is in the kitchen"],["wait", 0.5],["say", "We are already in the kitchen"],["move", "Kitchen"]],"officeliving room": [["say", "The _object is in the Living Room"],["wait", 0.5],["say", "you can get to the Living Room by the door to my right."],["wait", 0.5],["say", "let me show you"],["move", "office-living room"],["say", "We are entering the living room. The couch is on my right and The Coffee Table is in front of me"],["move", "LivingRoom"]],"bedroomliving room": [["say", "The _object is in the Living Room"],["wait", 0.5],["say","you can get to the Living Room by the door behind me and then going through the left doorway"],["wait", 0.5],["say", "let me show you"],["move", "bedroom-office"],["say", "We are entering the office. The desk is in front of me and The coat hanger is on my right"],["move", "office-living room"],["say", "We are entering the living room. The couch is on my right and The Coffee Table is in front of me"],["move", "living room"]],"living roomliving room": [["say", "The _object is in the LivingRoom"],["wait", 0.5],["say", "We are already in the LivingRoom"],["move", "living room"]],"kitchenliving room": [["say", "The _object is in the Living Room"],["wait", 0.5],["say", "you can get to the Living Room by the door to my right."],["wait", 0.5],["say", "let me show you"],["move", "kitchen-living room"],["say", "We are entering the living room. The TV is on my left and The sideboard is on my right"],["move", "living room"]],"officeoffice": [["say", "The _object is in the office"],["wait", 0.5],["say", "We are already in the office"],["move", "office"]],"bedroomoffice": [["say", "The _object is in the office"],["wait", 0.5],["say", "you can get to the office by the door behind me."],["wait", 0.5],["say", "let me show you"],["move", "bedroom-office"],["say", "We are entering the office. The desk is in front of me and The coat hanger is on my right"],["move", "office"]],"living roomoffice": [["say", "The _object is in the office"],["wait", 0.5],["say", "you can get to the office by the door to my right."],["wait", 0.5],["say", "let me show you"],["move", "living room-office"],["say", "We are entering the office. The desk is on my left and The coat hanger is on my right"],["move", "office"]],"kitchenoffice": [["say", "The _object is in the office"],["wait", 0.5],["say", "you can get to the office by the door to my right and then going to your right again."],["wait", 0.5],["say", "let me show you"],["move", "kitchen-living room"],["say", "We are entering the living room. The TV is on my left and The sideboard is on my right"],["move", "living room-office"],["say", "We are entering the office. The desk is on my left and The coat hanger is on my right"],["move", "office"]],"officebedroom": [["say", "The _object is in the Bedroom"],["wait", 0.5],["say", "you can get to the Bedroom by the door to my right."],["wait", 0.5],["say", "let me show you"],["move", "office-bedroom"],["say", "We are entering the bedroom. The Bedroom chest is on my right and The Bed is in front of me"],["move", "bedroom"]],"bedroombedroom":[["say", "The _object is in the Bedroom"], ["wait", 0.5], ["say", "We are already in the Bedroom"], ["move", "bedroom"]],"living roombedroom": [["say", "The _object is in the Bedroom"],["wait", 0.5],["say","you can get to the Bedroom by the door in front of me and then going to your right"],["wait", 0.5],["say", "let me show you"],["move", "living room-office"],["say", "We are entering the office. The desk is on my left and The coat hanger is on my right"],["move", "office"],["move", "office-bedroom"],["say", "We are entering the bedroom. The Bedroom chest is on my right and The Bed is in front of me"],["move", "bedroom"]],"kitchenbedroom": [["say", "The _object is in the Bedroom"],["wait", 0.5],["say", "you can get to the Bedroom by the door behind me."],["wait", 0.5],["say", "let me show you"],["passdoor", "kitchen-bedroom"],["say", "We are entering the bedroom, the bed is in front of me and the bedroom chest is to my left."],["move", "bedroom"]]}


    def execute(self, userdata):

        '''Execute this state'''

        destinationKey = userdata.startingRoom+userdata.endingRoom
        seq = dictdirect[destinationKey]
        
        userdata.sequence = seq
        
        for index, order in enumerate(seq):
            seq[index][1] = seq[index][1].replace("_object", userdata.object)
        
        print(seq)

        # nothing to check
        return 'done'













































