import codecs
import json
import  pickle
import os
import shutil
import textwrap
import time

class FileControl:
    def __init__(self, emailTemplate, emailFrom):
        self.emailTemplate = emailTemplate
        self.emailFrom = emailFrom

    def ListDirs(self, root):
        if not os.path.isdir(root):
            return ""
        dirs = ""
        try:
            listD = os.listdir(root)
            for d in listD:
                dirs += d + '\n'
                dirs += self.ListDirs(root + d + "\\")
        except:
            return dirs
        return dirs

    def ShowTree(self, root):
        tree = []
        if not bool(root):
            for c in range(ord('A'), ord('Z') + 1):
                path = chr(c) + ":\\"
                if os.path.isdir(path):
                    tree.append(path)
        elif os.path.isdir(root):
            listD = os.listdir(root)
            for d in listD:
                tree.append(root + d)
        response = {
            "isSuccess": True,
            "message": tree
        }
        self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response)) 

    def DelFile(self, filePath):
        if os.path.exists(filePath):
            try:
                response = {
                    "isSuccess": True,
                    "message": "Deleted " + filePath
                }
                os.remove(filePath)
                self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            except:
                response = {
                    "isSuccess": False,
                    "message": "Failed to process from the server. Please try one more time."
                }
                self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
                return
        else:
            response = {
                    "isSuccess": False,
                    "message": "Path not Found! Please try one more time."
                }
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            return

    # copy file from client to server
    def CopyFileToServer(self, filePath):
        filePath = codecs.decode(filePath, 'unicode_escape')
        fileName = filePath.split("\\")[-1]

        source = os.path.join(os.getcwd() + '\\Downloads\\', fileName)
        os.rename(source, filePath)
        os.replace(source, filePath)
        shutil.move(source, filePath)

    # copy file from server to client
    def CopyFileToClient(self, filePath):
        if not bool(filePath) or not os.path.isfile(filePath):
            response = {
                "isSuccess": False,
                "message": "File not Found! Please try one more time."
            }
            
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            return
        response = {
            "isSuccess": True
        }
        filePath = codecs.decode(filePath, 'unicode_escape')
        fileName = filePath.split("\\")[-1]
        self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response), fileName = fileName, filePath = filePath)


    def FileHandle(self):       
        while True:
            time.sleep(5)
            requestContent = self.emailTemplate.Receive()
            if not requestContent:
                continue
            jsonContent = json.loads(requestContent)
            body = jsonContent["Body"]
            bodyJson = json.loads(body)
            data = bodyJson["Data"]


            if ("SHOW" in data):
                root = ""
                if "Root" in data:
                    root = data["Root"]
                self.ShowTree(root)
            
            # copy file from client to server
            elif ("COPYTO" in data):
                filename = ""
                if "Root" in data:
                    filename = data["Root"]
                self.CopyFileToServer(filename)

            # copy file from server to client
            elif ("COPY" in data):
                filename = ""
                if "Root" in data:
                    filename = data["Root"]
                self.CopyFileToClient(filename)

            elif ("DEL" in data):
                filePath = ""
                if "Root" in data:
                    filePath = data["Root"]
                self.DelFile(filePath)

            elif ("QUIT" in data):
                return
            
            else:
                self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
