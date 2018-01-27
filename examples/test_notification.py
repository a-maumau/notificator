from notificator import Notificator

# create a Notificator
notificator = Notificator()

# setup for notification from Slack
# all kind of parameter should be in secret.py
# see the secret_sample.py
notificator.setSlack()

# setup for notification from mail
# all kind of parameter should be in secret.py
# see the secret_sample.py
notificator.setMail()

# send notification with message "test notification." from all set up method.
notificator.send_notification("test notification.")
