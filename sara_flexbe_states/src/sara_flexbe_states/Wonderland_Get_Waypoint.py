#!/usr/bin/env python
# encoding=utf8

from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, Point, Quaternion
from tf import transformations

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
	#> pose         Pose2D   The pose of the waypoint

	<= done         return when at least one entity exist
	<= no_waypoint        return when no entity have the selected name
	<= error        return when error reading data
	'''
	
	def __init__(self, index_function):
		# See example_state.py for basic explanations.
		super(Wonderland_Get_Waypoint, self).__init__(outcomes=['done', 'no_waypoint', 'error'],
											input_keys=['json_text', 'input_value'],
											output_keys=['id', 'name', 'x', 'y', 'theta', 'pose'])

		self._index_function = index_function
		self._index = 0

	def execute(self, userdata):
		# parse parameter json data
		data = json.loads(userdata.json_text)

		# read if there is data
		if data is None:
			# continue to Zero
			print("Data is None")
			return 'error'

		# read if there is data
		if len(list(data)) == 0:
			# continue to Zero
			print("No waypoint was found")
			return 'error'

		# try to read data
		if 'id' not in data:
			# continue to Error
			print("No ID")
			return 'error'

		if 'name' not in data:
			# continue to Error
			print("No NAME")
			return 'error'

		if 'x' not in data:
			# continue to Error
			print("No X")
			return 'error'

		if 'y' not in data:
			# continue to Error
			print("No Y")
			return 'error'

		if 'theta' not in data:
			# continue to Error
			print("No THETA")
			return 'error'

		# write return datas
		userdata.id = data['id']
		userdata.name = data['name']
		userdata.x = data['x']
		userdata.y = data['y']
		userdata.theta = data['theta']

		pt = Point(data['x'], data['y'], 0)
		qt = transformations.quaternion_from_euler(0, 0, data['theta'])
		userdata.pose = Pose(position=pt, orientation=Quaternion(*qt))

		# continue to Done
		return 'done'
	
	def on_enter(self, userdata):
		if self._index_function is not None:
			try:
				self._index = self._index_function(userdata.input_value)
			except Exception as e:
				Logger.logwarn('Failed to execute index function!\n%s' % str(e))
