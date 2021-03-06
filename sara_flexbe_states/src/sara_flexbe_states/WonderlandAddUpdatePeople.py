#!/usr/bin/env python
# encoding=utf8

import json

import requests
from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core import EventState, Logger
from sara_msgs.msg import Entities
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion
from math import tan
"""
Created on 17/05/2018

@author: Lucas Maurice
"""


class WonderlandAddUpdatePeople(EventState):
    '''
    Add or update all known persons in wonderland.

    <= done                     return when the add correctly append
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandAddUpdatePeople, self).__init__(outcomes=['done'])
        self.url = "http://wonderland:8000/api/people/"

        self._sub = ProxySubscriberCached({'/entities': Entities})

        self._topic = "/robot_pose"
        self._subscriber_pos = ProxySubscriberCached({self._topic: Pose})
        self.my_pose = None
        self.message = None

    def execute(self, userdata):

        if self._subscriber_pos.has_msg(self._topic):
            self.my_pose = self._subscriber_pos.get_last_msg(self._topic)

        if self._sub.has_msg('/entities'):
            Logger.loginfo('getting message')
            self.message = self._sub.get_last_msg('/entities')
            self._sub.remove_last_msg('/entities')

        if self.message is not None and self.my_pose is not None:
            for person in self.message.entities:
                if person.name == "person":
                    result = self.add_person(person)

                    # If people already exist
                    if result == 1:
                        result = self.update_person(person)

                        # Error during person update.
                        if result != 0:
                            Logger.logerr("An error happen during people update.")

                    # Error during person add.
                    elif result < 0:
                        Logger.logerr("An error happen during people add.")

        return 'done'

    def add_person(self, entity):
        data = {}

        # Prepare request

        if entity.ID is not None:
            data.update({'peopleRecognitionId': entity.ID})

        if entity.color is not None:
            data.update({'peopleColor': entity.color})

        if entity.color is not None:
            data.update({'peopleColor': entity.color})

        if entity.pose is not None:
            data.update({'peoplePose': entity.pose})

        if entity.poseProbability is not None:
            data.update({'peoplePoseAccuracy': entity.poseProbability})

        if entity.face.gender is not None:
            data.update({'peopleGender': entity.face.gender})

        if entity.face.genderProbability is not None:
            data.update({'peopleGenderAccuracy': entity.face.genderProbability})

        if entity.face.emotion is not None:
            data.update({'peopleEmotion': entity.face.emotion})

        if entity.face.emotionProbability is not None:
            data.update({'peopleEmotionAccuracy': entity.face.emotionProbability})

        if entity.face.emotion is not None:
            data.update({'peopleEmotion': entity.face.emotion})

        if entity.face.emotionProbability is not None:
            data.update({'peopleEmotionAccuracy': entity.face.emotionProbability})

        if entity.isOperator is None:
            data.update({'peopleIsOperator': False})
        else:
            data.update({'peopleIsOperator': entity.isOperator})

        if len(entity.aliases) > 0:
            data.update({'peopleName': entity.aliases[0]})

        # try the request
        try:
            response = requests.post(self.url, data=data)
            if response.status_code == 201:
                return 0

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                data = json.loads(response.content)
                if 'peopleRecognitionId' in data and data['peopleRecognitionId'][0] \
                        == u'people with this peopleRecognitionId already exists.':
                    return 1
                else:
                    return -1
            else:
                Logger.logerr(response.status_code)
                return -1

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return -1

    def update_person(self, entity):
        data = {}

        # Prepare request

        if entity.wonderlandId is None and entity.ID is None:
            Logger.logwarn('Need wonderland ID or face ID !')
            return 'bad_request'

        if entity.wonderlandId is not None:
            data.update({'peopleId': entity.wonderlandId})

        if entity.ID is not None:
            data.update({'peopleRecognitionId': entity.ID})

        if entity.color is not None:
            data.update({'peopleColor': entity.color})

        if entity.pose is not None:
            data.update({'peoplePose': entity.pose})

        if entity.poseProbability is not None:
            data.update({'peoplePoseAccuracy': entity.poseProbability})

        if entity.face.gender is not None:
            data.update({'peopleGender': entity.face.gender})

        if entity.face.genderProbability is not None:
            data.update({'peopleGenderAccuracy': entity.face.genderProbability})

        if entity.face.emotion is not None:
            data.update({'peopleEmotion': entity.face.emotion})

        if entity.face.emotionProbability is not None:
            data.update({'peopleEmotionAccuracy': entity.face.emotionProbability})

        if entity.isOperator is not None:
            data.update({'peopleIsOperator': entity.isOperator})

        if len(entity.aliases) > 0:
            data.update({'peopleName': entity.aliases[0]})

        # try the request
        try:
            response = requests.patch(self.url, data=data)
            if response.status_code == 200:
                return 0

            elif response.status_code == 404:
                Logger.logwarn("Bad Request")
                return 1

            elif 400 <= response.status_code < 500:
                Logger.logwarn(response.status_code)
                Logger.logwarn("Bad Request")
                return -1

            else:
                Logger.logerr(response.status_code)
                Logger.logwarn("Bad Request")
                return -1

        except requests.exceptions.RequestException as e:
            Logger.logerr(e)
            return -1
