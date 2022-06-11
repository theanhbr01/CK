import os


class ShutdownRestartControl:
    @staticmethod
    def LoadData(data):
        global action

        action = '' 

        if("Action" in data):
            action = data["Action"]

    @staticmethod
    def Handle(data):
        try:
            ShutdownRestartControl.LoadData(data)
            if "SHUTDOWN" == action:
                os.system("shutdown /s /t 1")
                return {
                    'isSuccess': True,
                    "message": "Shutting down..."
                }
            elif "RESTART" == action:
                os.system("shutdown /r")
                return {
                    'isSuccess': True,
                    "message": "Restarting... "
                }
            else:
                return
            return
        except:
            return {
                    "isSuccess": False,
                    "message":  "Failed to process from the server. Please try one more time."
                }