# in case python2
from __future__ import print_function

import threading

from .notification import MailNotification, SlackNotification, TwitterNotification
from . import secret

class Notificator:
	def __init__(self, suppress_err=True):
		self._notificators = []
		self.suppress_err = suppress_err
		self._set_mail = False
		self._set_slack = False
		self._set_twitter = False

	# set default mail notification, which is written in secret.py
	def setMail(self):
		if not self._set_mail:
			self._notificators.append(MailNotification(secret.MAIL_PASSWORD, secret.MAIL_ACCOUNT, secret.MAIL_TO_ADDRESS, secret.MAIL_BCC_ADDRESS, secret.MAIL_SUBJECT, self.suppress_err))
			self._set_mail = True

	def addMailNotify(self, passwd, account, to_addr, bcc_addr, subject, suppress_err=True):
		self._notificators.append(MailNotification(passwd, account, to_addr, bcc_addr, subject, suppress_err))

	# set default Slack notification, which is written in secret.py
	def setSlack(self):
		if not self._set_slack:
			self._notificators.append(SlackNotification(secret.SLACK_USER_NAME, secret.SLACK_CHANNEL, secret.SLACK_HOOK_URL, self.suppress_err))
			self._set_slack = True

	def addSlackNotify(self, user_name, channel, hook_url, suppress_err=True):
		self._notificators.append(SlackNotification(user_name, channel, hook_url, suppress_err))

	# set default Twitter notification, which is written in secret.py
	def setTwitter(self):
		if not self._set_twitter
			self._notificators.append(TwitterNotification(secret.API_KEY, secret.API_SECRET, secret.ACCESS_TOKEN, secret.ACCESS_SECRET, self.suppress_err))
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
