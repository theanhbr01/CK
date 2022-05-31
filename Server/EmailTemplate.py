import email
import imaplib
import smtplib
from email.mime.text import MIMEText

class EmailTemplate:
    receiveUrl = 'imap.gmail.com'
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL(self.receiveUrl)
        self.mail.login(self.username, self.password)

    def Receive(self):
        try:
            self.mail.select('inbox')
            status, data = self.mail.search(None, '(UNSEEN)')
            mail_ids = []

            for block in data:
                mail_ids += block.split()

            for i in mail_ids:

                status, data = self.mail.fetch(i, '(RFC822)')

                for response_part in data:
                    if isinstance(response_part, tuple):

                        message = email.message_from_bytes(response_part[1])

                        mail_from = message['from']
                        mail_subject = message['subject']

                        if message.is_multipart():
                            mail_body = ''

                            for part in message.get_payload():

                                if part.get_content_type() == 'text/plain':
                                    mail_body += part.get_payload()
                        else:
                            mail_body = message.get_payload()

                        response = dict()
                        response["From"] = mail_from
                        response["Subject"] = mail_from
                        response["Body"] = mail_body

                        return response
        except:
            print("An exception occurred!")
            return
    
    def SendNotification(self, emailFrom, emailTo, emailCc = "", emailBcc = "", emailReplyTo = "", useHTML = False, subject = "", body =""):
        try:
            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = emailFrom
            message['To'] = emailTo
            message['CC'] = emailCc
            message['BCC'] = emailBcc
            message['In-Reply-To'] = emailReplyTo

            # we'll connect using SSL
            server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
            # to interact with the server, first we log in
            # and then we send the message
            server.login(self.username, self.password)
            server.sendmail(emailFrom, emailTo, message.as_string())
            server.quit()
        except:
            print("An exception occurred!")
            return