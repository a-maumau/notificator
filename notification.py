# in case python2
from __future__ import print_function

import abc

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import json
import requests
from requests_oauthlib import OAuth1Session

class NotificationTemplate(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, suppress_err=True):
		self.suppress_err = suppress_err

	@abc.abstractmethod
	def send_message(self, msg):
		# arg should be str 
		raise NotImplementedError()

	@abc.abstractmethod
	def contents(self):
		# return the setting str for debug or interact
		raise NotImplementedError()

	def setMentionUsers(self, user_names):
		# set mention str like "@user_name"
		pass

class MailNotification(NotificationTemplate):
	"""
		only testing on Gmail account.
		change SMTP_ADDRESS and SMTP_PORT for your use.
	"""
	SMTP_ADDRESS = 'smtp.gmail.com'
	SMTP_PORT = 587   # for TLS
	#SMTP_PORT = 465  # for SSL
	
	def __init__(self, passwd, from_addr, to_addr, bcc_addr, subject, suppress_err=True):
		"""
			from_addr = 'sender@gmail.com'
			passwd    = 'password'
			to_addr   = 'receiver@example.com'
			bcc_addr  = 'receiver2@example.com'
			subject   = 'test mail from python'
			body      = 'Hi! This mail is sent from python script!'
		"""
		super().__init__(suppress_err)

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
			if not self.suppress_err:
				import traceback
				traceback.print_exc()
				print(e)
				print("which means, could not send a notification mail...")
	
	def contents(self):
		return "account:{}, to:{}, bcc:{}, subject:{}".format(self._from_addr, self._to_addr, self._bcc_addr, self._subject)

class SlackNotification(NotificationTemplate):
	def __init__(self, user_name, channel, hook_url, suppress_err=True):
		"""
			user_name = 'user_name'
			channel   = 'which channel you want to post'
			hook_url  = 'api's web hook url
		"""
		super().__init__(suppress_err)

		self.user_name = user_name
		self.channel = channel
		self.hook_url = hook_url
		self.mention_users = ""

	def setMentionUsers(self, user_names):
		self.mention_users = user_names

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
				if not self.suppress_err:
					# if it's not success, show the code
					print("(Slack) error code : {}".format(resp.status_code))
		
		except Exception as e:
			if not self.suppress_err:
				import traceback
				traceback.print_exc()
				print(e)

	def contents(self):
		return "user_name:{}, channel:{}, mention:{}".format(self.user_name, self.channel, self.mention_users)

class TwitterNotification(NotificationTemplate):
	post_url = "https://api.twitter.com/1.1/statuses/update.json"

	def __init__(self, api_key, api_secret, access_token, access_secret, suppress_err=True):
		"""
			you need get the api_key, api_secret, access_token, access_secret
			from twitter developer.
		"""
		super().__init__(suppress_err)

		self.api_key = api_key
		self.api_secret = api_secret
		self.access_token = access_token
		self.access_secret = access_secret
		self.mention_users = ""
		self.twitter = OAuth1Session(self.api_key, self.api_secret, self.access_token, self.access_secret)

	def setMentionUsers(self, user_names):
		self.mention_users = user_names

	def send_message(self, msg):
		try:
			# be careful for posting same sentence, witch cause 403 error.
			resp = self.twitter.post(self.post_url, params={"status":msg})
			if resp.ok != True:
				if not self.suppress_err:
					# if it's not success, show the code
					print("(Twitter) error code : {}".format(resp.status_code))

		except Exception as e:
			if not self.suppress_err:
				import traceback
				traceback.print_exc()
				print(e)

	def contents(self):
		return "mention:{}".format(self.mention_users)
