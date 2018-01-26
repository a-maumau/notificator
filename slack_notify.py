# in case python2
from __future__ import print_function

import sys
import argparse

from datetime import datetime

import pytz
from pytz import all_timezones_set

# import notificator class
from notificator import Notificator

def notificate_by_slack(msg="notification"):
	# create a Notificator
	notificator = Notificator()

	# setup for notification from Slack
	# all kind of parameter should be in secret.py
	# see the secret_sample.py
	notificator.setSlack()

	# send notification with message "test notification." from all set up method.
	notificator.send_notification(msg)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='notificate.py [--msg "notification message"| -msg_from_input]', epilog="")
	
	parser.add_argument('--msg', type=str, default="notification.", help='notification message')
	parser.add_argument('-msg_from_input', action="store_true", default=False, help='use the pipe or redirection input for msg.')
	
	parser.add_argument('--timezone', type=str, default="UTC", help='set time zone.\ndefault is "UTC".\nexample: "Asia/Tokyo"\nit must be in the time zone list in pytz.all_timezones_set\nuse option "--list_timezone" to see whole list.')
	parser.add_argument('--list_timezone', action="store_true", default=False, help='show the list of time zones, which are in the pytz.all_timezones_set')
	parser.add_argument('-timestamp', action="store_true", default=False, help='add a time stamp')
	
	args = parser.parse_args()
	
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
		now = datetime.now()
	
	time_stamp = now.strftime('%Y/%m/%d %H:%M:%S %Z %z')
	
	# which means input is from pipe or redirection
       	if sys.stdin.isatty() == False:
		nonttyinput = sys.stdin.read()
        
	if args.msg_from_input:
		args.msg = nonttyinput
	
	notificate_by_slack(args.msg + ("\n[start time: {}]".format(time_stamp)) if args.timestamp else "")
