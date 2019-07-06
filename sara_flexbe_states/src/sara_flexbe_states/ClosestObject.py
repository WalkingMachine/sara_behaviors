#!/usr/bin/env python
# encoding=utf8

import json

import requests,math
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entity, Entities


"""
Created on 05/07/2019

@author: Huynh-Anh Le
"""


class ClosestObject(EventState):
    '''
    Read the position of a room in a json string
    ># object             the object to be found         Recognition name of the object

    <= found              return when one entity exist
    <= not_found             return when no entity exist

    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(ClosestObject, self).__init__(outcomes=['found', 'not_found'],
                                                        input_keys=['object'],
                                                        output_keys=['angle','closestObject'])
        self.entities = []

    def execute(self, userdata):

        angle, closest = self.getclosest(userdata.object)
        userdata.closestObject = closest
        userdata.angle = angle

        if closest:
            return "found"
        else:
            return "not_found"


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


    def getclosest(self,item):
        min = 100000

        item=self.getEntities(item,"")[0]

        for i in self.getEntities("",""):
            if i.wonderlandId != item.wonderlandId :
                distance = ((item.waypoint.x - i.waypoint.x) ** 2 +
                  (item.waypoint.y - i.waypoint.y) ** 2) ** 0.5

        #trouve lobjet le plus proche

            if(distance < min):
                min = distance
                closest = i

        dx = item.x- closest.x
        dy = item.y-closest.y
        angle = math.atan2(dy,dx)



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
