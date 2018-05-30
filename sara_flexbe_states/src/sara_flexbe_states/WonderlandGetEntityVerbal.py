#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core import EventState
from rospy import logerr, logwarn, loginfo
from sara_msgs.msg import Entity, Entities

"""
Created on 15/05/2018

@author: Lucas Maurice
"""


class WonderlandGetEntityVerbal(EventState):
    '''
    Read the position of a room in a json string
    ># name             string         Recognition name of the object
    ># containers       string array   Array of containers recognition name (can be empty) on single container

    #> entities         sara_msgs/Entities   list of entities

    <= one              return when one entity exist
    <= multiple         return when more than one entity exist
    <= none             return when no entity exist
    <= error            return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetEntityVerbal, self).__init__(outcomes=['one', 'multiple', 'none', 'error'],
                                                        input_keys=['name', 'containers'],
                                                        output_keys=['entities'])

    def execute(self, userdata):
        # Generate URL to contact

        if type(userdata.name) is str:
            url = "http://wonderland:8000/api/entity?entityClass=" + str(userdata.name)
        else:
            url = "http://wonderland:8000/api/entity?none"

        if type(userdata.containers) is str:
            url += "&entityContainer=" + userdata.containers

        elif type(userdata.containers) is list:
            for container in userdata.containers:
                if type(container) is str:
                    url += "&entityContainer=" + container

        logwarn(url)

        # try the request
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logerr(e)
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)

        loginfo(data)

        if len(data) == 0:
            return 'none'

        elif len(data) == 1 and 'entityId' in data[0]:
            userdata.entities = self.generateEntity(data[0])
            return 'one'

        elif 'entityId' in data:
            userdata.entities = self.generateEntity(data)
            return 'one'

        else:
            entities = Entities()

            for entityData in data:
                if 'entityId' in entityData:
                    entities.entities.append(self.generateEntity(entityData))

            userdata.entities = entities
            return 'multiple'

    def generateEntity(self, data):
        entity = Entity()

        entity.wonderlandId = data['entityId']
        if 'entityName' in data:
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
        entity.waypoint.theta = data['entityWaypointYaw']

        entity.containerId = data['entityContainer']

        loginfo(entity)

        return entity
