# !/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState
from sara_msgs.msg import Entity

"""
Created on 15/05/2018

@author: Lucas Maurice
"""


class GenerateEntity(EventState):
    '''
    Add a person.
    --  ID                      The
    --  wonderlandId            The
    --  aliases                 The
    --  name                    The
    --  category                The
    --  color                   The
    --  weight                  The
    --  size                    The
    --  position_x              The
    --  position_y              The
    --  position_z              The
    --  waypoint_x              The
    --  waypoint_y              The
    --  waypoint_theta          The
    --  velocity_x              The
    --  velocity_y              The
    --  velocity_z              The
    --  containerId             The
    --  face_id                 The
    --  face_gender             The
    --  face_genderProbability  The
    --  face_emotion            The
    --  face_emotionProbability The
    --  pose                    The
    --  poseProbability         The
    --  isOperator              The

    #>  entity                  sara_msgs/Entity

    <= done                     return when the add correctly append
    '''

    def __init__(self, ID, wonderlandId, aliases, name, category, color, weight, size,
                 position_x, position_y, position_z, waypoint_x, waypoint_y, waypoint_theta,
                 velocity_x, velocity_y, velocity_z, containerId,
                 face_id, face_gender, face_genderProbability, face_emotion, face_emotionProbability,
                 pose, poseProbability, isOperator):
        # See example_state.py for basic explanations.
        super(GenerateEntity, self).__init__(output_keys=['entity'], outcomes=['done'])

        self.ID = ID
        self.wonderlandId = wonderlandId
        self.aliases = aliases
        self.name = name
        self.category = category
        self.color = color
        self.weight = weight
        self.size = size
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.waypoint_x = waypoint_x
        self.waypoint_y = waypoint_y
        self.waypoint_theta = waypoint_theta
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z
        self.containerId = containerId
        self.face_id = face_id
        self.face_gender = face_gender
        self.face_genderProbability = face_genderProbability
        self.face_emotion = face_emotion
        self.face_emotionProbability = face_emotionProbability
        self.pose = pose
        self.poseProbability = poseProbability
        self.isOperator = isOperator

    def execute(self, userdata):
        entity = Entity()

        entity.ID = self.ID
        entity.wonderlandId = self.wonderlandId
        entity.aliases.append(self.aliases)
        entity.name = self.name
        entity.category = self.category
        entity.color = self.color
        entity.weight = self.weight
        entity.size = self.size
        entity.position.x = self.position_x
        entity.position.y = self.position_y
        entity.position.z = self.position_z
        entity.waypoint.x = self.waypoint_x
        entity.waypoint.y = self.waypoint_y
        entity.waypoint.theta = self.waypoint_theta
        entity.velocity.x = self.velocity_x
        entity.velocity.y = self.velocity_y
        entity.velocity.z = self.velocity_z
        entity.containerId = self.containerId
        entity.face.id = self.face_id
        entity.face.gender = self.face_gender
        entity.face.genderProbability = self.face_genderProbability
        entity.face.emotion = self.face_emotion
        entity.face.emotionProbability = self.face_emotionProbability
        entity.pose = self.pose
        entity.poseProbability = self.poseProbability
        entity.isOperator = self.isOperator

        userdata.entity = entity

        return 'done'
