#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
import json


class Wonderland_List_Something(EventState):
	'''
	Return all things IDs and Names
	
	># json_text    string  json to read
	
	#> names        float[] array containing all names
	#> ids          int[]   array containing all IDs
	
	<= done         return when the list contain at least one object
	<= empty        return when the list is empty
	<= error        return when error reading data
	'''
	
	def __init__(self):
		# See example_state.py for basic explanations.
		super(Wonderland_List_Something, self).__init__(outcomes=['done', 'empty', 'error'],
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
			names.append(data['name'])
			ids.append(data['id'])
		
		userdata.names = names
		userdata.ids = ids
		
		# continue to Done
		return 'done'