#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json

class Wonderland_Read_Entity(EventState):
	'''
	Read the 3D position of an entity in a json string
	-- index_function   function	index of the
	># input_value      object	Input to the index function.
	># json_text        string  command to read
	#> id               int     id on the BDD of the object
	#> name             string  name of the object
	#> time             string  time of the last update
	#> x_pos            float   x position of the entity
	#> y_pos            float   y position of the entity
	#> z_pos            float   z position of the entity
	<= done             return when at least one entity exist
	<= empty            return when no entity have the selected name
	<= error            return when error reading data
	'''
	
	def __init__(self, index_function):
		super(Wonderland_Read_Entity, self).__init__(outcomes=['done', 'empty', 'error'],
													input_keys=['json_text', 'input_value'],
													output_keys=['id', 'name', 'time', 'x_pos', 'y_pos', 'z_pos', 'waypoint_id'])
		self._index_function = index_function
		self._index = 0
	
	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)
		
		# read if there is data
		if not data[self._index]:
			# continue to Zero
			return 'empty'
		
		# try to read data
		if 'id' not in data[self._index]:
			# continue to Error
			return 'error'
		
		if 'name' not in data[self._index]:
			# continue to Error
			return 'error'
		
		if 'time' not in data[self._index]:
			# continue to Error
			return 'error'

		if 'x' not in data[self._index]:
			# continue to Error
			return 'error'
		
		if 'x' not in data[self._index]:
			# continue to Error
			return 'error'
		
		if 'y' not in data[self._index]:
			# continue to Error
			return 'error'
		
		if 'z' not in data[self._index]:
			# continue to Error
			return 'error'


		# write return datas
		userdata.id = data[self._index]['id']
		userdata.name = data[self._index]['name']
		userdata.time = data[self._index]['time']
		userdata.x_pos = data[self._index]['x']
		userdata.y_pos = data[self._index]['y']
		userdata.z_pos = data[self._index]['z']

		if 'waypoint' in data[self._index]:
			if 'id' in data[self._index]['waypoint']:
				userdata.waypoint_id = data[self._index]['waypoint']['id']

		# continue to Done
		return 'done'
	
	def on_enter(self, userdata):
		if self._index_function is not None:
			try:
				self._index = self._index_function(userdata.input_value)
			except Exception as e:
				Logger.logwarn('Failed to execute index function!\n%s' % str(e))