from notificator import Notificator

notificator = Notificator()

notificator.setSlack()
notificator.setMail()

notificator.send_notification("test notification.")

