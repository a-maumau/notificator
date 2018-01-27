# in case python2
from __future__ import print_function

import json
import requests

from .notificator_template import NotificatorTemplate

class SlackNotificator(NotificatorTemplate):
	def __init__(self, user_name, channel, hook_url):
		self.user_name = user_name
		self.channel = channel
		self.hook_url = hook_url

	def send_message(self, msg):
		# the permission of app directly affect this point.
		content = {"username" : self.user_name,
			   "channel"  : self.channel,
			   "text"     : msg
                	  }
		"""
			other parameter like "icon_emoji":':grim:'...
			for detail see https://api.slack.com/methods/chat.postMessage
			
			this doesn't work anymore ?
				to use mention like '@here', use <!channel> <!user_name>
			
			deprecated parameter
				"link_names" : True use insted <@user_name> util 2018.9, after this use <@user_id>?
		"""

		try:
			resp = requests.post(self.hook_url, data=json.dumps(content))
			if resp.ok != True:
				# if it's not success, show the code
				print("error code : {}".format(resp.status_code))
		
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)

if __name__=='__main__':
	print("nothing here.")
