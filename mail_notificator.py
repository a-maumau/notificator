"""
only testing on Gmail account.
change SMTP_ADDRESS and SMTP_PORT for your use.
"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

from .notificator_template import NotificatorTemplate

SMTP_ADDRESS = 'smtp.gmail.com'
SMTP_PORT = 587   # for TLS
#SMTP_PORT = 465  # for SSL

"""
from_addr = 'sender@gmail.com'
passwd    = 'password'
to_addrs  = 'receiver@example.com'
bcc_addrs = 'receiver2@example.com'
subject   = 'test mail from python'
body      = 'Hi! This mail is sent from python script!'
"""

class MailNotificator(NotificatorTemplate):
    def __init__(self, passwd, from_addr, to_addr, bcc_addrs, subject):
        # set mail content
        self._passwd    = passwd
        self._from_addr = from_addr
        self._to_addr   = to_addr
        self._bcc_addrs = bcc_addrs
        self._subject   = subject

        # Actually, I don't know what it should be...
        self.charset = "iso-2022-jp"

    def _create_message(self, body):
        msg = MIMEText(body, "plain", self.charset)

        msg['Subject'] = self._subject
        msg['From']    = self._from_addr
        msg['To']      = self._to_addr
        msg['Bcc']     = self._bcc_addrs
        msg['Date']    = formatdate()

        return msg

    def send_message(self, msg):
        mail_content = self._create_message(msg)

        try:
            smtpobj = smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT)
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


if __name__ == '__main__':
    print("nothing here.")