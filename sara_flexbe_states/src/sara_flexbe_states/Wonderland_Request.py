#!/usr/bin/env python
# encoding=utf8

import requests
from flexbe_core import EventState, Logger


class Wonderland_Request(EventState):
	'''
	Send requests to Wonderland server
	
	># url      string  command to read
	#> response string  Finish job.
	
	<= done     data read correctly
	<= error    error while data is reading
	'''
	
	def __init__(self):
		super(Wonderland_Request, self).__init__(outcomes=['done', 'error'], input_keys=['url'], output_keys=['response'])
		# generate post key for authentication
		self._header = {'api-key': 'asdf'}
	
	def execute(self, userdata):
		# Generate URL to contact
		url = "http://192.168.0.46:8000/api/" + userdata.url
		
		# try the request
		try:
			response = requests.get(url, headers=self._header)
		except requests.exceptions.RequestException as e:
			print e
			return 'error'
		
		# read and return content
		userdata.response = response.content
		return 'done'
