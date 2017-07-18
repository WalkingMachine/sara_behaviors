#!/usr/bin/env python
# encoding=utf8

import json
import requests
from flexbe_core import EventState, Logger


class Wonderland_Add_Human(EventState):
	'''
	Add an human to Wonderland. For the room, enter only ID or Name, not both.
	Return the ID of the added human.

	># name             string  name of the human
	># roomID           string  ID on the BDD or name of the room
	># x_pos            int     Position on X
	># y_pos            int     Position on Y
	># z_pos            int     Position on Z
	># gender           string  Gender of the person
	># is_operator      boolean Say if it is the operator

	#> id               int     ID on the BDD of the human

	<= done     data sent correctly
	<= error    error while data is reading
	'''
	
	def __init__(self):
		super(Wonderland_Add_Human, self).__init__(outcomes=['done', 'error'],
		                                           output_keys=['id'],
		                                           input_keys=['name', 'roomID', 'x_pos', 'y_pos', 'z_pos', 'gender',
		                                                       'is_operator'])
		# generate post key for authentication
		self._header = {'api-key': 'asdf'}
	
	def execute(self, userdata):
		# Generate URL to contact
		
		if isinstance(userdata.roomID, (int, long)):
			dataPost = {'name': userdata.name, 'x': userdata.x_pos, 'y': userdata.y_pos, 'z': userdata.z_pos,
			            'gender': userdata.gender, 'operator': userdata.is_operator, 'roomID': userdata.roomID}
		else:
			dataPost = {'name': userdata.name, 'x': userdata.x_pos, 'y': userdata.y_pos, 'z': userdata.z_pos,
			            'gender': userdata.gender, 'operator': userdata.is_operator, 'roomName': userdata.roomID}
		
		# try the request
		try:
			response = requests.post("http://192.168.0.46:8000/api/human/", headers=self._header, data=dataPost)
		except requests.exceptions.RequestException as e:
			print e
			return 'error'
		
		# read response
		data_response = json.loads(response.content)
		
		# have a response
		if not data_response["entity"]:
			return 'error'
		
		# have an id to read
		if 'id' not in data_response["entity"]:
			# continue to Error
			return 'error'
		
		# return the ID
		userdata.id = data_response["entity"]['id']
		
		return 'done'
