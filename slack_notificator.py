import json
import requests

from notificator_template import NotificatorTemplate

class SlackNotificator(NotificatorTemplate):
	def __init__(self, user_name, channel, hook_url):
		self.user_name = user_name
		self.channel = channel
		self.hook_url = hook_url

	def send_message(self, msg):
		content = {"username": self.user_name,
				   "channel" : self.channel,
				   "text"    : msg}
		# other parameter : "icon_emoji":':grim:' , "channel" : 'general'

		try:
			resp = requests.post(self.hook_url, data=json.dumps(content))
			if resp.ok != True:
				print("error code : {}".format(resp.status_code))
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)

# Incoming Webhooksを使って対象のチャンネルにメッセージを送付
if __name__=='__main__':
	print("nothing here.")