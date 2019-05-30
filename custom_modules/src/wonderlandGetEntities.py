#!/usr/bin/env python

import json
import requests
from sara_msgs.msg import Entity
from flexbe_core import EventState, Logger

'''
Created on 29.05.2019

@author: Philippe La Madeleine
'''

def getEntitiesFromNameAndContainer(name, containers):
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
            entities.append(generateEntity(entityData))

    return entities


def generateEntity(data):
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
