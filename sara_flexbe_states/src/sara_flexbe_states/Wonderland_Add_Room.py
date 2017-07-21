#!/usr/bin/env python
# encoding=utf8

import json
import requests
from flexbe_core import EventState, Logger


class Wonderland_Add_Room(EventState):
	'''
	Add a room to Wonderland.
	Return the ID of the added room.

	#> name         string  name of the room
	#> x1           float   position of the room
	#> x2           float   position of the room
	#> x3           float   position of the room
	#> x4           float   position of the room
	#> y1           float   position of the room
	#> y2           float   position of the room
	#> y3           float   position of the room
	#> y4           float   position of the room

	#> id           int     ID on the BDD of the room

	<= done                 data sent correctly
	<= error                error while data is reading
	<= already_registered
	'''
	
	def __init__(self):
		super(Wonderland_Add_Room, self).__init__(outcomes=['done', 'already_registered', 'error'],
													output_keys=['id'],
													input_keys=['name', 'x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4'])
		# generate post key for authentication
		self._header = {'api-key': 'asdf'}
	
	def execute(self, userdata):
		# Generate URL to contact
		dataPost = {'name': userdata.name, 'x1': userdata.x1, 'x2': userdata.x2, 'x3': userdata.x3,'x4': userdata.x4,
					'y1': userdata.y1, 'y2': userdata.y2, 'y3': userdata.y3, 'y4': userdata.y4}
		
		# try the request
		try:
			response = requests.post("http://192.168.0.46:8000/api/rooms/", headers=self._header, data=dataPost)
		except requests.exceptions.RequestException as e:
			print e
			return 'error'
		
		# read response
		data_response = json.loads(response.content)
		
		# have a response
		if not data_response:
			return 'error'
		
		# have an a name ID to read
		if 'id' not in data_response and 'name' not in data_response:
			# continue to Error
			return 'error'
		
		# have an ID to read
		elif 'id' not in data_response:
			return 'already_registered'
		
		# return the ID
		userdata.id = data_response['id']
		
		return 'done'
