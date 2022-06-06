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

    def clean(text):
    # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

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
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        # subject, encoding = decode_header(msg["Subject"])[0]
                        # if isinstance(subject, bytes):
                        #     # if it's a bytes, decode to str
                        #     subject = subject.decode(encoding)
                        # # decode email sender
                        # From, encoding = decode_header(msg.get("From"))[0]
                        # if isinstance(From, bytes):
                        #     From = From.decode(encoding)
                        From = msg['from']
                        subject = msg['subject']
                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    # body = part.get_payload(decode=True).decode()
                                    if content_type == 'text/plain':
                                        body = part.get_payload()
                                except:
                                    pass
                                if "attachment" in content_disposition:
                                    # download attachment
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
                # open the file to be sent 
                attachment = open(filePath, "rb")
                
                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')
                
                # To change the payload into encoded form
                p.set_payload((attachment).read())
                
                # encode into base64
                encoders.encode_base64(p)
                
                p.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
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