# in case python2
from __future__ import print_function

import os
import threading
import yaml

from .notification import MailNotification, SlackNotification, TwitterNotification

class Notificator:
	def __init__(self, secrets="~/.secrets/notificator_secrets.yaml", suppress_err=True):
		"""
			secrets: path to your secret .yaml, or dictionary which contains the secrets
				for mail keys
					"MAIL_PASSWORD", "MAIL_ACCOUNT", "MAIL_TO_ADDRESS", "MAIL_BCC_ADDRESS", "MAIL_SUBJECT"
				for slack keys
					"SLACK_USER_NAME", "SLACK_CHANNEL", "SLACK_HOOK_URL"
				for twitter keys
					"API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_SECRET"
		"""
		self._notificators = []
		self.suppress_err = suppress_err
		self._set_mail = False
		self._set_slack = False
		self._set_twitter = False

		if isinstance(secrets, str):
			if os.path.exists(os.path.expanduser(secrets)):
				with open(os.path.expanduser(secrets), "r") as f:
					self.secrets = yaml.load(f)
		else:
			self.secrets = secrets


	# set default mail notification, which is written in secret.py
	def setMail(self):
		if not self._set_mail:
			self._notificators.append(MailNotification(self.secrets["MAIL_PASSWORD"], self.secrets["MAIL_ACCOUNT"], self.secrets["MAIL_TO_ADDRESS"], self.secrets["MAIL_BCC_ADDRESS"], self.secrets["MAIL_SUBJECT"], self.suppress_err))
			self._set_mail = True

	def addMailNotify(self, passwd, account, to_addr, bcc_addr, subject, suppress_err=True):
		self._notificators.append(MailNotification(passwd, account, to_addr, bcc_addr, subject, suppress_err))

	# set default Slack notification, which is written in secret.py
	def setSlack(self):
		if not self._set_slack:
			self._notificators.append(SlackNotification(self.secrets["SLACK_USER_NAME"], self.secrets["SLACK_CHANNEL"], self.secrets["SLACK_HOOK_URL"], self.suppress_err))
			self._set_slack = True

	def addSlackNotify(self, user_name, channel, hook_url, suppress_err=True):
		self._notificators.append(SlackNotification(user_name, channel, hook_url, suppress_err))

	# set default Twitter notification, which is written in secret.py
	def setTwitter(self):
		if not self._set_twitter
			self._notificators.append(TwitterNotification(self.secrets["API_KEY"], self.secrets["API_SECRET"], self.secrets["ACCESS_TOKEN"], self.secrets["ACCESS_SECRET"], self.suppress_err))
			self._set_twitter = True

	def addTwitterNotify(self, api_key, api_secret, access_token, access_secret, suppress_err=True):
		self._notificators.append(TwitterNotification(api_key, api_secret, access_token, access_secret, suppress_err))

	def show_list(self):
		for idx, noti in enumerate(self._notificators):
			print("{:3} : {}".format(idx, noti.contents()))

	def del_notify(self, idx):
		if idx < len(self._notificators) and idx >= 0:
			_ = self._notificators.pop(idx)
			return True
		return False

	def get_list(self):
		return self._notificators

	def _send_notification(self, msg):
		# broadcast notification
		for noti in self._notificators:
			noti.send_message(msg)

	def notify(self, msg, use_thread=False):
		# sometimes it take time, so if you want low latency, set use_thread=True
		if use_thread:
			try:
				th = threading.Thread(target=self._send_notification, args=(msg,))
				th.start()
			except Exception as e:
				import traceback
				traceback.print_exc()
				print(e)
		else:
			self._send_notification(msg)
