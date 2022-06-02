import codecs
import json
import  pickle
import os
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

    # # copy file from client to server
    # def CopyFileToServer(self):
    #     request = self.emailTemplate.Receive()
    #     p = request.body
    #     if (received == "-1"):
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
    #         return
    #     filename, filesize, path = received.split(SEPARATOR)
    #     filename = os.path.basename(filename)
    #     filesize = int(filesize)
    #     data = b""
    #     while len(data) < filesize:
    #         packet = sock.recv(999999)
    #         data += packet
    #     if (data == "-1"):
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
    #         return
    #     try:
    #         with open(path + filename, "wb") as f:
    #             f.write(data)
    #     except:
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")

    # copy file from server to client
    def CopyFileToClient(self, filePath):
        if not bool(filePath) or not os.path.isfile(filePath):
            response = {
                "isSuccess": False,
                "message": "File not Found! Please try one more time."
            }
            filePath = codecs.decode(filePath, 'unicode_escape')
            fileName = filePath.split("\\")[-1]
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            return
        response = {
            "isSuccess": True
        }
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
            
            # # copy file from client to server
            # elif (mod == "COPYTO"):
            #     self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "OK")
            #     self.CopyFileToServer(client)
            #     isMod = False

            # copy file from server to client
            elif (data == "COPY"):
                filename = ""
                if "Root" in data:
                    filename = data["Root"]
                self.CopyFileToClient(filename)

            elif (data == "DEL"):
                filePath = ""
                if "Root" in data:
                    filePath = data["Root"]
                self.DelFile(filePath)

            elif (data == "QUIT"):
                return
            
            else:
                self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
