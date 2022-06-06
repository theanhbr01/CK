import datetime
import pyautogui
import os, sys

class ScreenshotControl:
    @staticmethod
    def abs_path(file_name):
        file_name = 'screenshot//' + file_name + '.png'
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, file_name)

    @staticmethod
    def Handle():
        try:
            now = datetime.datetime.now()
            fileName = now.strftime("%d_%m_%Y_%H_%M_%S")
            filePath = ScreenshotControl.abs_path(fileName)

            pic = pyautogui.screenshot()
            pic.save(filePath)
            return {
                "isSuccess": True,
                "fileName": fileName,
                "filePath": filePath
            }
        except:
            return {
                    "isSuccess": False,
                    "message":  "Failed to process from the server. Please try one more time."
                }

