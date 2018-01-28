# in case python2
from __future__ import print_function

import threading

from .notification import MailNotification, SlackNotification
from . import secret

class Notificator:
	def __init__(self):
		self._notificators = []

	# set default mail notification, which is written in secret.py
	def setMail(self):
		self._notificators.append(MailNotification(secret.MAIL_PASSWORD, secret.MAIL_ACCOUNT, secret.MAIL_TO_ADDRESS, secret.MAIL_BCC_ADDRESS, secret.MAIL_SUBJECT))

	def addMailNotify(self, passwd, account, to_addr, bcc_addr, subject):
		self._notificators.append(MailNotification(passwd, account, to_addr, bcc_addr, subject))

	# set default Slack notification, which is written in secret.py
	def setSlack(self):
		self._notificators.append(SlackNotification(secret.SLACK_USER_NAME, secret.SLACK_CHANNEL, secret.SLACK_HOOK_URL))

	def addSlackNotify(self, user_name, channel, hook_url):
		self._notificators.append(SlackNotification(user_name, channel, hook_url))

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
