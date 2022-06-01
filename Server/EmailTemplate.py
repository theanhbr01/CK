import json
import email
import imaplib
import os
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

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
                fileName = ""
                status, data = self.mail.fetch(i, '(RFC822)')
                raw_email = data[0][1]

                # converts byte literal to string removing b''
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                # downloading attachments
                for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet... 
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    if bool(fileName):
                        filePath = os.path.join(os.getcwd() + '\\Downloads\\', fileName)
                        if not os.path.exists(os.getcwd() + '\\Downloads\\'):
                            os.makedirs(os.getcwd() + '\\Downloads\\')
                        if not os.path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()

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

                        content = {
                            "From": mail_from,
                            "Subject": mail_from,
                            "Body": mail_body,
                            "FileAttachment": fileName
                        }

                        return json.dumps(content)
                        
        except:
            print("An exception occurred!")
            return
    
    def SendNotification(self, emailFrom, emailTo, emailCc = "", emailBcc = "", emailReplyTo = "", subject = "", body ="", fileName = "", filePath = ""):
        try:
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = emailFrom
            message['To'] = emailTo
            message['CC'] = emailCc
            message['BCC'] = emailBcc
            message['In-Reply-To'] = emailReplyTo
            message.attach(MIMEText(body, 'plain'))
            if(bool(fileName) and bool(filePath)):
                # open the file to be sent 
                filename = "File_name_with_extension"
                attachment = open("Path of the file", "rb")
                
                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')
                
                # To change the payload into encoded form
                p.set_payload((attachment).read())
                
                # encode into base64
                encoders.encode_base64(p)
                
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                message.attach(p)
                
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