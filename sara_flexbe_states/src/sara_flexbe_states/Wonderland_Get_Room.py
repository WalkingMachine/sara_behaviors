#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import requests
import json
from geometry_msgs.msg import Pose, Point
from tf.transformations import quaternion_from_euler


class WonderlandGetObject(EventState):
    '''
    Get the informations of an room

    ># id    int    id of the room
    ># name    string    name of the room
    ># type    string    category of the room
    ># expected_pose    pose/point    expected position of the room

    #> room_pose     pose     the pose of the returned room
    #> room_name    string    name of the room
    #> room_type    string    category of the room

    <= found         room     found
    <= unknown       the room is unknown
    <= error        return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(WonderlandGetObject, self).__init__(outcomes=['found', 'unknown', 'error'],
                                                  input_keys=['id', 'name', 'type', 'expected_pose'],
                                                  output_keys=['id', 'room_pose', 'room_name', 'room_type'])
        self._index = 0
        self._header = {'api-key': 'asdf'}

    def execute(self, userdata):

        # Generate URL to contact
        url = "http://wonderland:8000/api/room/?"
        if userdata.id != None:
            url += "id=" + str(userdata.id) + "&"
        if userdata.name != None:
            url += "name=" + str(userdata.name) + "&"
        if userdata.type != None:
            url += "type=" + str(userdata.type) + "&"
        if userdata.expected_pose == None:
            Logger.logerr("in " + self.name + ", you must give an expected pose or point")
            return 'error'

        if type(userdata.expected_pose) is Pose:
            expX = userdata.expected_pose.position.x
            expY = userdata.expected_pose.position.y
            expZ = userdata.expected_pose.position.z
        elif type(userdata.expected_pose) is Point:
            expX = userdata.expected_pose.position.x
            expY = userdata.expected_pose.position.y
            expZ = userdata.expected_pose.position.z
        else:
            return 'error'

        # try the request
        try:
            response = requests.get(url, headers=self._header)
        except requests.exceptions.RequestException as e:
            Logger.logerr(str(e))
            return 'error'

        # parse parameter json data
        data = json.loads(response.content)
        print "data:"
        print data
        if len(data) == 0:
            return 'unknown'

        # find the nearest room
        bestScore = 1000000
        best = None
        for d in data:
            print d
            score = ((expX - d['x_position']) ** 2 + (expY - d['y_position']) ** 2 + (
            expZ - d['z_position']) ** 2) ** 0.5
            if score < bestScore:
                bestScore = score
                best = d

        # generate the output pose
        pose = Pose()
        pose.position.x = best['x_position']
        pose.position.y = best['y_position']
        pose.position.z = best['z_position']
        quat = quaternion_from_euler(0, 0, best['theta'])
        pose.orientation.x = quat[0]
        pose.orientation.y = quat[1]
        pose.orientation.z = quat[2]
        pose.orientation.w = quat[3]

        # send the outputs
        userdata.room_id = best['id']
        userdata.room_pose = pose
        userdata.room_name = best['name']
        userdata.room_type = best['type']

        return 'found'
