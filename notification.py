# in case python2
from __future__ import print_function

import abc

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import json
import requests

class NotificationTemplate(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def send_message(self, msg):
		raise NotImplementedError()

	@abc.abstractmethod
	def contents(self):
		raise NotImplementedError()

class MailNotification(NotificationTemplate):
	"""
		only testing on Gmail account.
		change SMTP_ADDRESS and SMTP_PORT for your use.
	"""
	SMTP_ADDRESS = 'smtp.gmail.com'
	SMTP_PORT = 587   # for TLS
	#SMTP_PORT = 465  # for SSL
	
	def __init__(self, passwd, from_addr, to_addr, bcc_addr, subject):
		"""
			from_addr = 'sender@gmail.com'
			passwd    = 'password'
			to_addr   = 'receiver@example.com'
			bcc_addr  = 'receiver2@example.com'
			subject   = 'test mail from python'
			body      = 'Hi! This mail is sent from python script!'
		"""
		# set mail content
		self._passwd = passwd
		self._from_addr = from_addr
		self._to_addr = to_addr
		self._bcc_addr = bcc_addr
		self._subject = subject

		# Actually, I don't know what it should be...
		self.charset = "iso-2022-jp"

	def _create_message(self, body):
		msg = MIMEText(body, "plain", self.charset)

		msg['Subject'] = self._subject
		msg['From'] = self._from_addr
		msg['To'] = self._to_addr
		msg['Bcc'] = self._bcc_addr
		msg['Date'] = formatdate()

		return msg

	def send_message(self, msg):
		mail_content = self._create_message(msg)

		try:
			# expecting using Gmail
			smtpobj = smtplib.SMTP(self.SMTP_ADDRESS, self.SMTP_PORT)
			smtpobj.ehlo()
			smtpobj.starttls()
			smtpobj.ehlo()
			smtpobj.login(self._from_addr, self._passwd)
			smtpobj.sendmail(self._from_addr, self._to_addr, mail_content.as_string())
			smtpobj.close()
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)
			print("which means, could not send a notification mail...")
	def contents(self):
		return "pass:********, account:{}, to:{}, bcc:{}, subject:{}".format(self._from_addr, self._to_addr, self._bcc_addr, self._subject)

class SlackNotification(NotificationTemplate):
	def __init__(self, user_name, channel, hook_url):
		"""
			user_name = 'user_name'
			channel   = 'which channel you want to post'
			hook_url  = 'api's web hook url
		"""
		self.user_name = user_name
		self.channel = channel
		self.hook_url = hook_url

	def send_message(self, msg):
		"""
			other parameter like "icon_emoji":':grim:'...
			for detail see https://api.slack.com/methods/chat.postMessage
			
			this doesn't work anymore ?
				to use mention like '@here', use <!channel> <!user_name>
			
			deprecated parameter
				"link_names" : True use insted <@user_name> util 2018.9, after this use <@user_id>?
		"""

		# the permission of app directly affect this point.
		content = {"username" : self.user_name,
				   "channel"  : self.channel,
				   "text"     : msg
				   }

		try:
			resp = requests.post(self.hook_url, data=json.dumps(content))
			if resp.ok != True:
				# if it's not success, show the code
				print("error code : {}".format(resp.status_code))
		
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)

	def contents(self):
		return "user_name:{}, channel:{}".format(self.user_name, self.channel)
