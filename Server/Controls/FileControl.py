import json
import  pickle
import os
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
        tree = ""
        if not bool(root):
            for c in range(ord('A'), ord('Z') + 1):
                path = chr(c) + ":\\"
                if os.path.isdir(path):
                    tree += path + '\n'
        elif os.path.isdir(root):
            listD = os.listdir(root)
            for d in listD:
                tree += root + d + '\n'
        self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = data)

    # def SendListDirs(self):
    #     request = self.emailTemplate.Receive()
    #     path = request.body
    #     if not os.path.isdir(path):
    #         return [False, path]

    #     try:
    #         listT = []
    #         listD = os.listdir(path)
    #         for d in listD:
    #             listT.append((d, os.path.isdir(path + "\\" + d)))
            
    #         data = pickle.dumps(listT)
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = data)
    #         return [True, path]
    #     except:
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "Failed to process from the server. Please try one more time.")
    #         return [False, "error"]    

    # def DelFile(self):
    #     request = self.emailTemplate.Receive()
    #     p = request.body
    #     if os.path.exists(p):
    #         try:
    #             os.remove(p)
    #             self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "ok")
    #         except:
    #             self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "Failed to process from the server. Please try one more time.")
    #             return
    #     else:
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "Failed to process from the server. Please try one more time.")
    #         return

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

    # # copy file from server to client
    # def CopyFileToClient(self):
    #     request = self.emailTemplate.Receive()
    #     filename = request.body
    #     if filename == "-1" or not os.path.isfile(filename):
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
    #         return
    #     with open(filename, "rb") as f:
    #         data = f.read()
    #         self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = data)


    def FileHandle(self):       
        while True:
            time.sleep(5)
            requestContent = self.emailTemplate.Receive()
            if not requestContent:
                continue
            jsonContent = json.loads(requestContent)
            body = jsonContent["Body"]
            bodyJson = json.loads(body)
            rawData = bodyJson["Data"]
            data = json.loads(rawData)

            if ("SHOW" in data):
                root = data["Root"]
                self.ShowTree(root)
            
            # # copy file from client to server
            # elif (mod == "COPYTO"):
            #     self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "OK")
            #     self.CopyFileToServer(client)
            #     isMod = False

            # # copy file from server to client
            # elif (data == "COPY"):
            #     self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "OK")
            #     self.CopyFileToClient(client)
            #     isMod = False

            # elif (data == "DEL"):
            #     self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "OK")
            #     self.DelFile(client)
            #     isMod = False

            elif (data == "QUIT"):
                return
            
            else:
                self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = "-1")
