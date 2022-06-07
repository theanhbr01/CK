import json
import email
import imaplib
import os
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

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
                From = ""
                subject = ""
                body = ""
                status, msg = self.mail.fetch(i, '(RFC822)')
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        From = msg['from']
                        subject = msg['subject']
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    if content_type == 'text/plain':
                                        body = part.get_payload()
                                except:
                                    pass
                                if "attachment" in content_disposition:
                                    fileName = part.get_filename()
                                    if fileName:
                                        filePath = os.path.join(os.getcwd() + '\\Downloads\\', fileName)
                                        if not os.path.exists(os.getcwd() + '\\Downloads\\'):
                                            os.makedirs(os.getcwd() + '\\Downloads\\')
                                        if not os.path.isfile(filePath) :
                                            fp = open(filePath, 'wb')
                                            fp.write(part.get_payload(decode=True))
                                            fp.close()
                content = {
                            "From": From,
                            "Subject": subject,
                            "Body": body,
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
                attachment = open(filePath, "rb")
                
                p = MIMEBase('application', 'octet-stream')
                
                p.set_payload((attachment).read())
                
                encoders.encode_base64(p)
                
                p.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
                message.attach(p)
                
            server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
            server.login(self.username, self.password)
            server.sendmail(emailFrom, emailTo, message.as_string())
            server.quit()
        except:
            print("An exception occurred!")
            return