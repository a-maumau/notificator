# secrets and other setting.

# Gmail should be the best.(well, be honest, I only tested on Gmail...)
# if you want to use other mail, please rewrite the mail_notification.py
"""
	if you are not using "2-Step Verification",
	you need to accept the
		"Let less secure apps use your account"
	on your google account.
	I recommend "2-Step Verification", and set that password
"""
MAIL_PASSWORD    = "set pass word of GMAIL_ACCOUNT"
MAIL_ACCOUNT     = "your_address@gmail.com"
MAIL_TO_ADDRESS  = "mail address you want to send a notification mail"
MAIL_BCC_ADDRESS = "bcc address"
MAIL_SUBJECT     = "subject of the mail"

# slack
# you need get your own application Webhook URL
# for the permission of App for slack that you made, it don't always affect the settings. 
SLACK_USER_NAME = "slack user name"
SLACK_CHANNEL   = "#channel or @channel"
SLACK_HOOK_URL  = "hook url for app"

#Twitter
API_KEY = "consumer/api key"
API_SECRET = "consumer/api secret"
ACCESS_TOKEN = "access token"
ACCESS_SECRET = "access secret"
