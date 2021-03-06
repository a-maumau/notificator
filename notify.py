"""
	all in one pack python code.
	for lazy people.
"""
# in case python2
from __future__ import print_function

import os
import sys
import threading

import abc
import argparse

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import json
import yaml
import requests
from requests_oauthlib import OAuth1Session

from datetime import datetime
import pytz
from pytz import all_timezones_set

# rewrite for your use, or use the .yaml file
# Gmail should be the best.(well, be honest, I only tested on Gmail...)
# if you want to use other mail service, please rewrite the codes, sorry...
"""
	if you are not using "2-Step Verification",
	you need to accept the
		"Let less secure apps use your account"
	on your google account.
	I recommend "2-Step Verification", and set that password
"""
secrets = {
	"MAIL_PASSWORD"    : "set pass word of GMAIL_ACCOUNT",
	"MAIL_ACCOUNT"     : "your_address@gmail.com",
	"MAIL_TO_ADDRESS"  : "mail address you want to send a notification mail",
	"MAIL_BCC_ADDRESS" : "bcc address",
	"MAIL_SUBJECT"     : "subject of the mail",

	# slack
	# you need get your own application Webhook URL
	# for the permission of App for slack that you made, it don't always affect the settings. 
	"SLACK_USER_NAME" : "slack user name",
	"SLACK_CHANNEL"   : "#channel or @channel",
	"SLACK_HOOK_URL"  : "hook url for app",

	#Twitter
	"API_KEY"       : "consumer/api key",
	"API_SECRET"    : "consumer/api secret",
	"ACCESS_TOKEN"  : "access token",
	"ACCESS_SECRET" : "access secret",
}

class NotificationTemplate(object):
	__metaclass__ = abc.ABCMeta

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
				# if it's not success, show the code
				print("error code : {}".format(resp.status_code))
		
		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)

	def contents(self):
		return "user_name:{}, channel:{}, mention:{}".format(self.user_name, self.channel, self.mention_users)

class TwitterNotification(NotificationTemplate):
	post_url = "https://api.twitter.com/1.1/statuses/update.json"

	def __init__(self, api_key, api_secret, access_token, access_secret):
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
			resp = self.twitter.post(self.post_url, params={"status": msg})
			if resp.ok != True:
				# if it's not success, show the code
				print("error code : {}".format(resp.status_code))

		except Exception as e:
			import traceback
			traceback.print_exc()
			print(e)

	def contents(self):
		return "mention:{}".format(self.mention_users)

class Notificator:
	secrets = secrets
	def __init__(self, yaml_secrets=None):
		self._notificators = []
		if yaml_secrets is not None:
			self.secrets = yaml_secrets

	# set default mail notification, which is written in secret.py
	def setMail(self):
		self._notificators.append(MailNotification(self.secrets["MAIL_PASSWORD"], self.secrets["MAIL_ACCOUNT"], self.secrets["MAIL_TO_ADDRESS"], self.secrets["MAIL_BCC_ADDRESS"], self.secrets["MAIL_SUBJECT"]))

	def addMailNotify(self, passwd, account, to_addr, bcc_addr, subject):
		self._notificators.append(MailNotification(passwd, account, to_addr, bcc_addr, subject))

	# set default Slack notification, which is written in secret.py
	def setSlack(self):
		self._notificators.append(SlackNotification(self.secrets["SLACK_USER_NAME"], self.secrets["SLACK_CHANNEL"], self.secrets["SLACK_HOOK_URL"]))

	def addSlackNotify(self, user_name, channel, hook_url):
		self._notificators.append(SlackNotification(user_name, channel, hook_url))

	# set default Twitter notification, which is written in secret.py
	def setTwitter(self):
		self._notificators.append(TwitterNotification(self.secrets["API_KEY"], self.secrets["API_SECRET"], self.secrets["ACCESS_TOKEN"], self.secrets["ACCESS_SECRET"]))

	def addTwitterNotify(self, api_key, api_secret, access_token, access_secret):
		self._notificators.append(TwitterNotification(api_key, api_secret, access_token, access_secret))

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

def notificate(msg, args, yaml_secrets=None):
	# create a Notificator
	notificator = Notificator(yaml_secrets)

	if args.nomail == False:
		# all kind of parameter should be in secret
		notificator.setMail()

	if args.noslack == False:
		# all kind of parameter should be in secret
		notificator.setSlack()

	if args.notwitter == False:
		# all kind of parameter should be in secret
		notificator.setTwitter()

	# send notification with message
	notificator.notify(msg)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='notify.py [option]\nuse it for your convenient and save time.', epilog="")
	
	parser.add_argument('--yaml_path', type=str, default="~/.secrets/notificator_secrets.yaml", help='read from .yaml file. default is ~/.secrets/notificator_secrets.yaml')

	parser.add_argument('--msg', type=str, default="notification of the end of something", help='notification message')
	parser.add_argument('--msg_begin', type=str, default="notification of the begin of something", help='notification message begining of the job or smething')
	parser.add_argument('-msg_from_input', action="store_true", default=False, help='use the pipe or redirection input for msg.')
	
	parser.add_argument('--timezone', type=str, default="UTC", help='set time zone.\ndefault is "UTC".\nexample: "Asia/Tokyo"\nit must be in the time zone list in pytz.all_timezones_set\nuse option "--list_timezone" to see whole list.')
	parser.add_argument('--list_timezone', action="store_true", default=False, help='show the list of time zones, which are in the pytz.all_timezones_set')
	parser.add_argument('-timestamp', action="store_true", default=False, help='add a time stamp')
	parser.add_argument('-mention_begin', action="store_true", default=False, help='send mention begin of the script')

	parser.add_argument('-nomail', action="store_true", default=False, help="won't use mail")
	parser.add_argument('-noslack', action="store_true", default=False, help="won't use slack")
	parser.add_argument('-notwitter', action="store_true", default=False, help="won't use twitter")

	args = parser.parse_args()

	if os.path.exists(os.path.expanduser(args.yaml_path)):
		with open(os.path.expanduser(args.yaml_path), "r") as f:
			yaml_secrets = yaml.load(f)
	else:
		yaml_secrets = None
	
	if args.list_timezone:
		print("##### time zone list #####")
		for time_zone in all_timezones_set:
			print(time_zone)
		exit()

	if args.timezone in all_timezones_set:
		tz = pytz.timezone(args.timezone)
		now = datetime.now(tz)
	else:
		print("{} is not in the all_timezones_set, so the time zone is set to UTC".format(args.timezone))
		tz = pytz.timezone("UTC")
		now = datetime.now(tz)
	
	start_time_stamp = now.strftime('%Y/%m/%d %H:%M:%S %Z %z')

	if args.mention_begin:
		notificate(msg="{}".format(args.msg_begin + ("\n[ begin: {}]".format(start_time_stamp) if args.timestamp else "")), args=args, yaml_secrets=yaml_secrets)
	
	# which means input is from pipe or redirection
	if sys.stdin.isatty() == False:
		nonttyinput = sys.stdin.read()
	
	if args.msg_from_input:
		args.msg = nonttyinput
	
	now = datetime.now(tz)
	end_time_stamp = now.strftime('%Y/%m/%d %H:%M:%S %Z %z')

	# send notification
	notificate(msg="{}".format(args.msg + ("\n[ begin: {}, end: {}]".format(start_time_stamp, end_time_stamp) if args.timestamp else "")), args=args, yaml_secrets=yaml_secrets)
