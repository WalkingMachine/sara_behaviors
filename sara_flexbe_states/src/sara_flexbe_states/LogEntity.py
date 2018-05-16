#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from sara_msgs.msg import Entity, Entities

"""
Created on 15/05/2018

@author: Lucas Maurice
"""


class LogEntity(EventState):
    '''
    Print an entity or entities object in Flexbe runtime. Should be only used for debug.
    ># entity           Entity  The entity or entities array following the `sara_msgs/entity.msg` structure

    <= done             returned when am error happen during the HTTP request
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(LogEntity, self).__init__(outcomes=['done'], input_keys=['entity'])

    def execute(self, userdata):
        if type(userdata.entity) is Entity:
            Logger.loginfo("=============== This is an entity. ===============")
            self.print_entity(userdata.entity)

        elif type(userdata.entity) is Entities:
            Logger.loginfo("=============== This is an entities array. ===============")
            for entity in userdata.entity.entities:
                Logger.loginfo("=============== This is an entity. ===============")
                self.print_entity(entity)

        return 'done'

    @staticmethod
    def print_entity(entity):
        Logger.loginfo("ID: " + str(entity.ID))

        Logger.loginfo("Wonderland ID: " + str(entity.wonderlandId))
        Logger.loginfo("Name: " + entity.name)

        for alias in entity.aliases:
            Logger.loginfo("Alias: " + alias)

        Logger.loginfo("Category: " + entity.category)
        Logger.loginfo("Color: " + entity.color)

        Logger.loginfo("Weight: " + str(entity.weight))
        Logger.loginfo("Size: " + str(entity.size))

        Logger.loginfo("Gender: " + entity.face.gender)
        Logger.loginfo("Gender probability" + str(entity.face.genderProbability) + "%")
        Logger.loginfo("Emotion: " + entity.face.emotion)
        Logger.loginfo("Emotion probability: " + entity.face.emotionProbability)
        Logger.loginfo("Face ID: " + str(entity.face.id))

        Logger.loginfo("Person Pose: " + entity.pose)
        Logger.loginfo("Person Pose Probability: " + str(entity.poseProbability))
        Logger.loginfo("Person is Operator: " + str(entity.isOperator))

        Logger.loginfo("Container ID: " + str(entity.containerId))

        Logger.loginfo("Position x: " + str(entity.position.x))
        Logger.loginfo("Position y: " + str(entity.position.y))
        Logger.loginfo("Position z: " + str(entity.position.z))

        Logger.loginfo("Waypoint x: " + str(entity.waypoint.x))
        Logger.loginfo("Waypoint y: " + str(entity.waypoint.y))
        Logger.loginfo("Waypoint yaw: " + str(entity.waypoint.theta))

        Logger.loginfo("Velocity x: " + str(entity.velocity.x))
        Logger.loginfo("Velocity y: " + str(entity.velocity.y))
        Logger.loginfo("Velocity z: " + str(entity.velocity.z))
