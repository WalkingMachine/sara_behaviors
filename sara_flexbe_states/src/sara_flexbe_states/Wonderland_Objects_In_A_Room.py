#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Objects_In_A_Room(EventState):
	'''
	Return all objects in a room
	
	># json_text        string  json to read
	
	#> names            int[]   array containing all names of objects in the room
	#> ids              id[]    array containing all IDs of objects in the room
	
	<= done             return when the room contain at least one object
	<= empty            return when the room is empty
	<= error            return when error reading data
	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Objects_In_A_Room, self).__init__(outcomes=['done', 'empty', 'error'],
		                                             input_keys=['json_text'],
		                                             output_keys=['ids', 'names'])
	
	def execute(self, userdata):
		# parse parameter json data
		datas = json.loads(userdata.json_text)
		
		# read if there is data
		if not datas:
			# continue to Zero
			return 'empty'
		
		names = []
		ids = []
		
		for data in datas:
			# try to read data
			if 'id' not in data:
				return 'error'
			
			# try to read data
			if 'name' not in data:
				return 'error'
			
			# write return datas
			names += [data['name']]
			ids += [data['id']]
		
		userdata.names=names
		userdata.ids=ids
		print str(names)[1:-1]
		print str(ids)[1:-1]
		
		# continue to Done
		return 'done'