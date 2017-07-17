#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json

class Wonderland_Read_Entity_Position(EventState):
	'''
	Read the 3D position of an entity in a json string

	># json_text    string  command to read
	
	#< x_pos        int  x position of the entity
	#< y_pos        int  y position of the entity
	#< z_pos        int  z position of the entity
	
	<= done         return when at least one entity exist
	<= zero         return when no entity have the selected name
	<= error        return when error reading data

	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Read_Entity_Position, self).__init__(outcomes=['done', 'zero', 'error'], input_keys=['json_text'],
			output_keys=['x_pos', 'y_pos', 'z_pos'])
	
	def execute(self, userdata):
		#parse parameter json data
		data = json.loads(userdata.json_text)
		
		#read if there is data
		if not data:
			#continue to Zero
			return 'zero'
		
		#try to read data
		if 'x' not in data[0]:
			#continue to Error
			return 'error'
		
		if 'y' not in data[0]:
			#continue to Error
			return 'error'
		
		if 'z' not in data[0]:
			#continue to Error
			return 'error'
		
		#write return datas
		userdata.x_pos = data[0]['x']
		userdata.y_pos = data[0]['y']
		userdata.z_pos = data[0]['z']
		
		#continue to Done
		return 'done'