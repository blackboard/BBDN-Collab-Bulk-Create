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

        self.yag = yagmail.SMTP(user=self.sender_email, password=self.password, host=self.server)


    def sendmail(self,to,html):
        receiver = to
        body = html.render()

        
        self.yag.send(
            to=receiver,
            subject=self.subject,
            contents=body,
)