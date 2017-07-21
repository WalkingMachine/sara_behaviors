#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Get_Waypoint(EventState):
	'''
	Read the position of a room in a json string
	-- index_function   function	index of the

	># json_text    string  command to read
	># input_value      object	Input to the index function.

	#> id           int     id of the waypoint
	#> name         string  name of the waypoint
	#> pos_x        float   position of the waypoint
	#> pos_y        float   position of the waypoint
	#> theta        float   angle of the waypoint

	<= done         return when at least one entity exist
	<= no_waypoint        return when no entity have the selected name
	<= error        return when error reading data
	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_Get_Waypoint, self).__init__(outcomes=['done', 'no_waypoint', 'error'],
											input_keys=['json_text', 'input_value'],
											output_keys=['id', 'name', 'pos_x', 'pos_y', 'theta'])
	
	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)
		
		# read if there is data
		if not data:
			# continue to Zero
			return 'no_waypoint'
		
		# try to read data
		if 'id' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'room_name' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'x1' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'x2' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'x3' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'x4' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'y1' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'y2' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'y3' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		if 'y4' not in data[self._id]['room']:
			# continue to Error
			return 'error'
		
		# write return datas
		userdata.id = data[self._id]['room']['id']
		userdata.name = data[self._id]['room']['room_name']
		userdata.x1 = data[self._id]['room']['x1']
		userdata.x2 = data[self._id]['room']['x2']
		userdata.x3 = data[self._id]['room']['x3']
		userdata.x4 = data[self._id]['room']['x4']
		userdata.y1 = data[self._id]['room']['y1']
		userdata.y2 = data[self._id]['room']['y2']
		userdata.y3 = data[self._id]['room']['y3']
		userdata.y4 = data[self._id]['room']['y4']
		
		# continue to Done
		return 'done'
	
	def on_enter(self, userdata):
		if self._id_function is not None:
			try:
				self._id = self._id_function(userdata.input_value)
			except Exception as e:
				Logger.logwarn('Failed to execute index function!\n%s' % str(e))