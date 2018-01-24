from mail_notificator import MailNotificator
from slack_notificator import SlackNotificator

import secret

class Notificator:
	def __init__(self):
		self._notificators = []

	def setSlack(self):
		self._notificators.append(SlackNotificator(secret.SLACK_USER_NAME, secret.SLACK_CHANNEL, secret.SLACK_HOOK_URL))

	def setMail(self):
		self._notificators.append(MailNotificator(secret.MAIL_PASSWORD, secret.MAIL_ACCOUNT, secret.MAIL_TO_ADDRESS, secret.MAIL_BCC_ADDRESS, secret.MAIL_SUBJECT))

	def send_notification(self, msg):
		for idx in range(len(self._notificators)):
			self._notificators[idx].send_message(msg)