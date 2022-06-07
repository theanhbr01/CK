import json
import os
import cv2
import datetime
import zipfile

class WebcamRecordControl:
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
    def CompressFile(fileName, filePath):
        fileNameWithoutExtention = os.path.splitext(fileName)[0]
        fileNameWithZipExtention = fileNameWithoutExtention + ".zip"

        filePathWithoutExtention = os.path.splitext(filePath)[0]
        filePathWithZipExtention = filePathWithoutExtention + ".zip"

        jungle_zip = zipfile.ZipFile(filePathWithZipExtention, 'w')
        jungle_zip.write(filePath, compress_type=zipfile.ZIP_DEFLATED)
        jungle_zip.close()
            
        os.remove(filePath)
        return fileNameWithZipExtention, filePathWithZipExtention

    @staticmethod
    def Handle(emailTemplate):
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
            vid = cv2.VideoCapture(0)

            while True:
                ret, frame = vid.read()

                out.write(frame)
                
                then = datetime.datetime.now()
                timeSpan = then - now
                if(timeSpan.total_seconds() > 600):
                    break

                WebcamRecordControl.LoadData(emailTemplate)

                if "STOP" == action:
                    break
            out.release()
            cv2.destroyAllWindows()
            compressedFileName, compressedFilePath = WebcamRecordControl.CompressFile(filename, filePath)
            return {
                "isSuccess": True,
                "fileName": compressedFileName,
                "filePath": compressedFilePath
            }

        except:
            return {
                    "isSuccess": False,
                    "message":  "Failed to process from the server. Please try one more time."
                }