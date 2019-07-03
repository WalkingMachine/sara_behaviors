#!/usr/bin/env python

import rospy
import json

from flexbe_core import EventState, Logger
from sara_msgs.msg import Entity, Entities
import requests

'''
Created on 18.03.2019

@author: Philippe La Madeleine
'''


class CheckMisplacedObjects(EventState):
    '''
    Keep all improperly placed objects from a list of entities.
    Use wonderland to detect if an object if not in it's expected position.

    -- position_tolerance  float    The minimal distance needed to consider an object "properly placed".

    ># entities  list               Input to the filter function

    #> expected_objects list        All expected objects.
    #> unexpected_objects list         All unexpected objects and their desired locations. ex: [[entity1, pseudo-entity of entity1 at the right place], [entity2, pseudo-entity of entity2 at the right place]]

    <= all_expected                 There are no unexpected objects.
    <= unexpected                   There are unexpected objects.

    '''

    def __init__(self, position_tolerance, default_destination="bin"):
        '''
        Constructor
        '''
        super(CheckMisplacedObjects, self).__init__(outcomes=['all_expected', 'unexpected'],
                                     input_keys=['entities'],
                                     output_keys=['expected_objects', 'unexpected_objects'])

        self.position_tolerance = position_tolerance
        self.default_destination = default_destination

    def execute(self, userdata):
        '''Execute this state'''

        correct, not_correct = self.filterEntities(userdata.entities)

        Logger.loginfo("correct: "+str(correct))
        Logger.loginfo("not_correct: "+str(not_correct))

        userdata.expected_objects = correct
        userdata.unexpected_objects = not_correct

        if len(not_correct) > 0:
            return 'unexpected'
        else:
            return 'all_expected'

    def filterEntities(self, entities):

        not_correct = []
        correct = []
        wonderland_buffer = {}
        wonderland_buffer_index = {}

        # Get the bin ID
        bine = self.getEntities(self.default_destination, [])[0]

        for entity in entities:

            if not wonderland_buffer.has_key(entity.name):
                wonderland_buffer[entity.name] = self.getEntities(entity.name, [])
                wonderland_buffer_index[entity.name] = 0

            wonderland_entities = wonderland_buffer[entity.name]
            print(type(wonderland_entities))
            if isinstance(wonderland_entities, (list, tuple)):
                if self.compareWithList(entity, wonderland_entities):
                    correct.append(entity)
                else:
                    if len(wonderland_buffer[entity.name]) != 0:
                        not_correct.append([entity, wonderland_entities[wonderland_buffer_index[entity.name]]])
                        wonderland_buffer_index[entity.name] = min(wonderland_buffer_index[entity.name]+1, len(wonderland_entities))
            else:
                not_correct.append([entity, bine])

        return correct, not_correct

    # Return true if there is at least one close entity
    def compareWithList(self, entity, entities):
        for en in entities:
            if self.compareEntities(entity, en):
                return True
        return False

    # Return true if the entities are close
    def compareEntities(self, entity1, entity2):
        dist = ((entity1.position.x - entity2.waypoint.x) ** 2
                + (entity1.position.y - entity2.waypoint.y) ** 2) ** 0.5
        Logger.loginfo("object "+str(entity1.name)+" and "+str(entity2.name)+" distance = "+str(dist))
        return dist < self.position_tolerance

    def getEntities(self, name, containers):
        # Generate URL to contact

        if type(name) is str:
            url = "http://wonderland:8000/api/entity?entityClass=" + str(name)
        else:
            url = "http://wonderland:8000/api/entity?none"

        if type(containers) is str:
            url += "&entityContainer=" + containers

        elif type(containers) is list:
            for container in containers:
                if type(container) is str:
                    url += "&entityContainer=" + container

        # try the request
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        entities = []
        for entityData in data:
            if 'entityId' in entityData:
                entities.append(self.generateEntity(entityData))

        return entities

    def generateEntity(self, data):
        entity = Entity()

        entity.wonderlandId = data['entityId']
        if 'entityName' in data and data['entityName'] is not None:
            entity.aliases.append(data['entityName'].encode('ascii', 'ignore'))

        # Description of the object:
        if 'entityClass' in data and data['entityClass'] is not None:
            entity.name = data['entityClass'].encode('ascii', 'ignore')
        if 'entityCategory' in data and data['entityCategory'] is not None:
            entity.category = data['entityCategory'].encode('ascii', 'ignore')
        if 'entityColor' in data and data['entityColor'] is not None:
            entity.color = data['entityColor'].encode('ascii', 'ignore')

        # Physical description of the object:
        entity.weight = data['entityWeight']
        entity.size = data['entitySize']

        # Location of the object
        entity.position.x = data['entityPosX']
        entity.position.y = data['entityPosY']
        entity.position.z = data['entityPosZ']
        # Add if needed: 'entityPosYaw' ; 'entityPosPitch' ; 'entityPosRoll'

        entity.waypoint.x = data['entityWaypointX']
        entity.waypoint.y = data['entityWaypointY']
        entity.waypoint.theta = data['entityWaypointYaw'] / 180 * 3.14159

        entity.containerId = data['entityContainer']

        return entity
