#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import requests
import json
from geometry_msgs.msg import Pose, Point
from tf.transformations import quaternion_from_euler

class GetObject(EventState):
    '''
    Get the informations of an object
    
    ># id    int    id of the object
    ># name    string    name of the object
    ># color    string    color of the object
    ># room    string    room of the object
    ># type    string    category of the object
    ># expected_pose    pose/point    expected position of the object
    
    #> object_pose     pose     the pose of the returned object
    #> object_name    string    name of the object
    #> object_color    string    color of the object
    #> object_room    string    room of the object
    #> object_type    string    category of the object

    <= found         object     found
    <= unknown       the object is unknown
    <= error        return when error reading data
    '''

    def __init__(self):
        # See example_state.py for basic explanations.
        super(GetObject, self).__init__(outcomes=['found', 'unknown', 'error'],
                                                              input_keys=['id', 'name', 'color', 'room', 'type', 'expected_pose'],
                                                              output_keys=['id', 'object_pose', 'object_name', 'object_color', 'object_room', 'object_type'])
        self._index = 0
        self._header = {'api-key': 'asdf'}

    def execute(self, userdata):

        # Generate URL to contact
        url = "http://wonderland:8000/api/object/?"
        if userdata.id != None:
            url += "id="+str(userdata.id)+"&"
        if userdata.name != None:
            url += "name="+str(userdata.name)+"&"
        if userdata.color != None:
            url += "color="+str(userdata.color)+"&"
        if userdata.room != None:
            url += "room="+str(userdata.room)+"&"
        if userdata.type != None:
            url += "type="+str(userdata.type)+"&"
        if userdata.expected_pose == None:
            Logger.logerr("in "+self.name+", you must give an expected pose or point")
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

        # find the nearest object
        bestScore = 1000000
        best = None
        for d in data:
            print d
            score = ((expX-d['x_position'])**2+(expY-d['y_position'])**2+(expZ-d['z_position'])**2)**0.5
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
        userdata.object_id = best['id']
        userdata.object_pose = pose
        userdata.object_name = best['name']
        userdata.object_color = best['color']
        userdata.object_type = best['type']

        return 'found'
