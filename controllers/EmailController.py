import logging
import yagmail
import getpass

class EmailController:

    def __init__(self, email_config):
        self.logger = logging.getLogger(name='email')

        self.server = email_config['smtpserver']
        self.sender_email = email_config['from']
        self.subject = email_config['subject']

        self.password = getpass.getpass("Please enter your email password: ")

    def sendmail(self,to,html):
        receiver = to
        body = html.render()

        yag = yagmail.SMTP(user=self.sender_email, password=self.password, host=self.server)

        yag.send(
            to=receiver,
            subject=self.subject,
            contents=body,
)