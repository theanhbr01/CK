import json
import os
import numpy as np
import pyautogui
import cv2
import datetime
import zipfile

class ScreenRecordControl:
    def __init__(self, emailTemplate, emailFrom):
        self.emailTemplate = emailTemplate
        self.emailFrom = emailFrom

    def CompressFile(self, fileName, filePath):
        fileNameWithoutExtention = os.path.splitext(fileName)[0]
        fileNameWithZipExtention = fileNameWithoutExtention + ".zip"

        filePathWithoutExtention = os.path.splitext(filePath)[0]
        filePathWithZipExtention = filePathWithoutExtention + ".zip"

        jungle_zip = zipfile.ZipFile(filePathWithZipExtention, 'w')
        jungle_zip.write(filePath, compress_type=zipfile.ZIP_DEFLATED)
        jungle_zip.close()
            
        os.remove(filePath)
        return fileNameWithZipExtention, filePathWithZipExtention

    def Handle(self):
        try:
            # Specify resolution
            resolution = (1920, 1080)
            
            # Specify video codec
            codec = cv2.VideoWriter_fourcc(*"XVID")

            # Specify name of Output file
            now = datetime.datetime.now()
            filename = now.strftime("%d_%m_%Y_%H_%M_%S") + ".avi"
            if not os.path.exists(os.getcwd() + '\\Recorder\\'):
                            os.makedirs(os.getcwd() + '\\Recorder\\')
            filePath = os.path.join(os.getcwd() + '\\Recorder\\', filename)
            # Specify frames rate. We can choose any 
            # value and experiment with it
            fps = 60.0
            
            
            # Creating a VideoWriter object
            out = cv2.VideoWriter(filePath, codec, fps, resolution)
            
            # Create an Empty window
            cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
            
            # Resize this window
            cv2.resizeWindow("Live", 480, 270)

            while True:
                # Take screenshot using PyAutoGUI
                img = pyautogui.screenshot()
            
                # Convert the screenshot to a numpy array
                frame = np.array(img)
            
                # Convert it from BGR(Blue, Green, Red) to
                # RGB(Red, Green, Blue)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
                # Write it to the output file
                out.write(frame)
                
                then = datetime.datetime.now()
                timeSpan = then - now
                if(timeSpan.total_seconds() > 600):
                    break

                requestContent = self.emailTemplate.Receive()
                if not requestContent:
                    continue
                jsonContent = json.loads(requestContent)
                body = jsonContent["Body"]
                bodyJson = json.loads(body)
                data = bodyJson["Data"]

                if "STOP" in data:
                    break
            out.release()
            cv2.destroyAllWindows()
            response = {
                "isSuccess": True
            }
            compressedFileName, compressedFilePath = self.CompressFile(filename, filePath)
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response), fileName = compressedFileName, filePath = compressedFilePath)
            return
        except:
            response = {
                    "isSuccess": False,
                    "message":  "Failed to process from the server. Please try one more time."
                }
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.username , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
            return