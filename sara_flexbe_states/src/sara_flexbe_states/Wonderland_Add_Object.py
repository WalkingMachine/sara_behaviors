#!/usr/bin/env python
# encoding=utf8

import json
import requests
from flexbe_core import EventState, Logger

# TODO: RENAME STATE

class Wonderland_Add_Object(EventState):
	'''
	Add an object to Wonderland.
	For the room, enter an integer ID or a string Name.
	Return the ID of the added/updated object.

	#> id       int         enter the id for edit or Null for add
	># name     string      name of the object
	># room     string/int  ID on the BDD or name of the room
	># x_pos    float       Position on X
	># y_pos    float       Position on Y
	># z_pos    float       Position on Z
	># z_pos    float       Position on Z

	#> id       int         ID on the BDD of the object

	<= done     data sent correctly
	<= error    error while data is reading
	'''

	def __init__(self):
		super(Wonderland_Add_Object, self).__init__(outcomes=['done', 'error'],
													output_keys=['id'],
													input_keys=['id', 'name', 'roomID', 'x_pos', 'y_pos', 'z_pos'])
		# generate post key for authentication
		self._header = {'api-key': 'asdf'}

	def execute(self, userdata):
		# Generate URL to contact
		if userdata.id is None:
			dataPost = {'name': userdata.name, 'x': userdata.x_pos, 'y': userdata.y_pos, 'z': userdata.z_pos}

			if isinstance(userdata.roomID, (int, long)):
				dataPost.update({'roomID': userdata.roomID})
			else:
				dataPost.update({'roomName': userdata.roomID})

			# try the request
			try:
				response = requests.post("http://wonderland:8000/api/object/", headers=self._header, data=dataPost)
			except requests.exceptions.RequestException as e:
				print e
				return 'error'
		else:
			dataPost = {'id': userdata.id}

			if userdata.name is not None:
				dataPost.update({'name': userdata.name})

			if userdata.x_pos is not None:
				dataPost.update({'x': userdata.x_pos})

			if userdata.y_pos is not None:
				dataPost.update({'y': userdata.y_pos})

			if userdata.z_pos is not None:
				dataPost.update({'z': userdata.z_pos})

			if isinstance(userdata.roomID, (int, long)):
				dataPost.update({'roomID': userdata.roomID})
			elif userdata.roomID is not None:
				dataPost.update({'roomName': userdata.roomID})

			# try the request
			try:
				response = requests.patch("http://192.168.0.46:8000/api/object/", headers=self._header, data=dataPost)
			except requests.exceptions.RequestException as e:
				print e
				return 'error'


		# read response
		data_response = json.loads(response.content)

		# have a response
		if data_response == "Error in ID given":
			return 'error'

		# have an id to read
		if 'id' not in data_response['entity']:
			# continue to Error
			return 'error'

		# return the ID
		userdata.id = data_response['entity']['id']
		return 'done'
