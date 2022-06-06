import codecs
import os

class FileControl:

    @staticmethod
    def ShowTree(root):
        tree = []
        if not bool(root):
            for c in range(ord('A'), ord('Z') + 1):
                path = chr(c) + ":\\"
                if os.path.isdir(path):
                    tree.append(path)
        elif os.path.isdir(root):
            listD = os.listdir(root)
            for d in listD:
                tree.append(root + d)
        return {
            "isSuccess": True,
            "message": tree
        }

    @staticmethod
    def DelFile(filePath):
        if os.path.exists(filePath):
            try:
                os.remove(filePath)
                return {
                    "isSuccess": True,
                    "message": "Deleted " + filePath
                }
            except:
                return {
                    "isSuccess": False,
                    "message": "Failed to process from the server. Please try one more time."
                }
        else:
            return {
                    "isSuccess": False,
                    "message": "Path not Found! Please try one more time."
                }
    @staticmethod
    # copy file from client to server
    def CopyFileToServer(filePath, fileName):
        # filePath = codecs.decode(filePath, 'unicode_escape')
        # fileName = filePath.split("\\")[-1]
        try:
            filePath = os.path.join(filePath, fileName)
            source = os.path.join(os.getcwd() + '\\Downloads\\', fileName)
            # if os.path.exists(filePath):
            #     if not os.path.exists(source):
            #         os.makedirs(source)
            os.rename(source, filePath)
            return {
                "isSuccess": True
            }
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

    # copy file from server to client
    @staticmethod
    def CopyFileToClient(filePath):
        try:
            if not bool(filePath) or not os.path.isfile(filePath):
                return {
                    "isSuccess": False,
                    "message": "File not Found! Please try one more time."
                }
                            
            
            filePath = codecs.decode(filePath, 'unicode_escape')
            fileName = filePath.split("\\")[-1]
            return {
                "isSuccess": True,
                "fileName": fileName,
                "filePath": filePath
            }
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

    @staticmethod
    def LoadData(data):
        global action
        global root

        root = ''
        action = ''

        if("Action" in data):
            action = data["Action"]
        if "Root" in data:
            root = data["Root"]

    @staticmethod
    def FileHandle(data, fileAttachment): 

        FileControl.LoadData(data)

        #Show dictionary tree
        if ("SHOW" == action):
            return FileControl.ShowTree(root)
        
        # copy file from client to server
        elif ("COPYTO" == action):
            return FileControl.CopyFileToServer(root, fileAttachment)

        # copy file from server to client
        elif ("COPY" == action):
            return FileControl.CopyFileToClient(root)
        #Delete the specific path
        elif ("DEL" == action):
            return FileControl.DelFile(root)
            
        else:
            return {
                "isSuccess": False,
                "message": "No action found with the " + action 
            }