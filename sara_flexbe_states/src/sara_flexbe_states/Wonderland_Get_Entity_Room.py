#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_Get_Entity_Room(EventState):
	'''
	Read the position of a room in a json string
	-- index_function   function	index of the
	
	># json_text    string  command to read
	># input_value      object	Input to the index function.

	#> id           int     id of the room
	#> name         string  name of the room
	#> x1           int     position of the room
	#> x2           int     position of the room
	#> x3           int     position of the room
	#> x4           int     position of the room
	#> y1           int     position of the room
	#> y2           int     position of the room
	#> y3           int     position of the room
	#> y4           int     position of the room

	<= done         return when at least one entity exist
	<= no_room        return when no entity have the selected name
	<= error        return when error reading data

	'''
	
	def __init__(self, index_function):
		# See example_state.py for basic explanations.
		super(Wonderland_Get_Entity_Room, self).__init__(outcomes=['done', 'no_room', 'error'],
		                                                      input_keys=['json_text', 'input_value'],
		                                                      output_keys=['id','name','x1','x2','x3','x4','y1','y2','y3','y4'])
		self._index_function = index_function
		self._index = 0
		
	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)
		
		# read if there is data
		if not data[self._index]:
			# continue to Zero
			return 'no_room'
		
		
		# try to read data
		if 'id' not in data[self._index]['room']:
			# continue to Error
			return 'error'

		if 'room_name' not in data[self._index]['room']:
			# continue to Error
			return 'error'

		if 'x1' not in data[self._index]['room']:
			# continue to Error
			return 'error'

		if 'x2' not in data[self._index]['room']:
			# continue to Error
			return 'error'

		if 'x3' not in data[self._index]['room']:
			# continue to Error
			return 'error'

		if 'x4' not in data[self._index]['room']:
			# continue to Error
			return 'error'
		
		if 'y1' not in data[self._index]['room']:
			# continue to Error
			return 'error'
		
		if 'y2' not in data[self._index]['room']:
			# continue to Error
			return 'error'
		
		if 'y3' not in data[self._index]['room']:
			# continue to Error
			return 'error'
		
		if 'y4' not in data[self._index]['room']:
			# continue to Error
			return 'error'
			
		# write return datas
		userdata.id = data[self._index]['room']['id']
		userdata.name = data[self._index]['room']['room_name']
		userdata.x1 = data[self._index]['room']['x1']
		userdata.x2 = data[self._index]['room']['x2']
		userdata.x3 = data[self._index]['room']['x3']
		userdata.x4 = data[self._index]['room']['x4']
		userdata.y1 = data[self._index]['room']['y1']
		userdata.y2 = data[self._index]['room']['y2']
		userdata.y3 = data[self._index]['room']['y3']
		userdata.y4 = data[self._index]['room']['y4']
		
		print data[self._index]['room']['id']
		print data[self._index]['room']['room_name']
		print data[self._index]['room']['x1']
		print data[self._index]['room']['x2']
		print data[self._index]['room']['x3']
		print data[self._index]['room']['x4']
		print data[self._index]['room']['y1']
		print data[self._index]['room']['y2']
		print data[self._index]['room']['y3']
		print data[self._index]['room']['y4']
		
		# continue to Done
		return 'done'
	
	def on_enter(self, userdata):
		if self._index_function is not None:
			try:
				self._index = self._index_function(userdata.input_value)
			except Exception as e:
				Logger.logwarn('Failed to execute index function!\n%s' % str(e))