#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Get_Doors(EventState):
	'''
	Import two doors
	># json_text        string  command to read
	
	#> entrance_id          float       ID of the entrance door
	#> entrance_x           float       X position of the entrance door
	#> entrance_y           float       Y position of the entrance door
	#> entrance_theta       float       Tetha of the entrance door
	#> entrance_rooms_id    float[]     IDs or rooms in front of entrance
	#> entrance_rooms_names string[]    Names or rooms in front of entrance
	
	#> exit_id              float       ID of the entrance door
	#> exit_x               float       X position of the entrance door
	#> exit_y               float       Y position of the entrance door
	#> exit_theta           float       Tetha of the entrance door
	#> exit_rooms_id        float[]     IDs or rooms in front of entrance
	#> exit_rooms_names     string[]    Names or rooms in front of entrance
	
	<= done                 return when at least one entity exist
	<= empty                return when no entity have the selected name
	<= error                return when error reading data

	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Get_Doors, self).__init__(outcomes=['done', 'error'], input_keys=['json_text'],
													output_keys=['entrance_id', 'entrance_x', 'entrance_y',
																'entrance_theta', 'entrance_rooms_id',
																'entrance_rooms_names','exit_id', 'exit_x', 'exit_y',
																'exit_theta', 'exit_rooms_id', 'exit_rooms_names'])

	def execute(self, userdata):
		# parse parameter json data
		datas = json.loads(userdata.json_text)
		
		# read if there is data
		if len(datas) < 2:
			# continue to Zero
			return 'error'
		
		# for all doors returned
		for data in datas:
			if 'id' not in data:
				return 'error'
				
			if 'x' not in data:
				return 'error'
			
			if 'y' not in data:
				return 'error'
			
			if 'theta' not in data:
				return 'error'
			
			if 'isExit' not in data:
				return 'error'
			
			if 'room' not in data:
				return 'error'

			temp_id = []
			temp_name = []
			for room in data['room']:
				temp_id.append(room['id'])
				temp_name.append(room['name'])
				
			if data['isExit']:
				userdata.entrance_id = data['id']
				userdata.entrance_x = data['x']
				userdata.entrance_y = data['y']
				userdata.entrance_theta = data['theta']
				userdata.entrance_rooms_id = temp_id
				userdata.entrance_rooms_names = temp_name
			else:
				userdata.exit_id = data['id']
				userdata.exit_x = data['x']
				userdata.exit_y = data['y']
				userdata.exit_theta = data['theta']
				userdata.exit_rooms_id = temp_id
				userdata.exit_rooms_names = temp_name

		# continue to Done
		return 'done'