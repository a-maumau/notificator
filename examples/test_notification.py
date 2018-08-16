from notificator import Notificator

# create a Notificator
# the secret should be in "~/.secrets/notificator_secrets.yaml" for default.
# for detail of .yaml, see "example/example.yaml"
notificator = Notificator(secrets="~/.secrets/notificator_secrets.yaml")

# setup notification from Slack
# all kinds of parameter should be in secret.py
# see the secret_sample.py
notificator.setSlack()

# setup notification from mail
# all kinds of parameter should be in secret.py
# see the secret_sample.py
notificator.setMail()

# setup notification from Twitter
# all kinds of parameter should be in secret.py
# see the secret_sample.py
notificator.setTwitter()

# send notification with message "test notification." from all set up method.
notificator.notify("test notification.")
