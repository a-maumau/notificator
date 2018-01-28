import threading

from .notification import MailNotification, SlackNotification
from . import secret

class Notificator:
	def __init__(self):
		self._notificators = []

	# set default Slack notification, which is written in secret.py
	def setSlack(self):
		self._notificators.append(SlackNotification(secret.SLACK_USER_NAME, secret.SLACK_CHANNEL, secret.SLACK_HOOK_URL))

	def addSlackNotify(self, user_name, channel, hook_url):
		self._notificators.append(SlackNotification(user_name, channel, hook_url))

	# set default mail notification, which is written in secret.py
	def setMail(self):
		self._notificators.append(MailNotification(secret.MAIL_PASSWORD, secret.MAIL_ACCOUNT, secret.MAIL_TO_ADDRESS, secret.MAIL_BCC_ADDRESS, secret.MAIL_SUBJECT))

	def addMailNotify(self, passwd, account, to_addr, bcc_addr, subject):
		self._notificators.append(MailNotification(passwd, account, to_addr, bcc_addr, subject))

	def _send_notification(self, msg):
		# broadcast notification
		for idx in range(len(self._notificators)):
			self._notificators[idx].send_message(msg)

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
