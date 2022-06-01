import re, winreg, json
import time
import os
class RegistryControl:
    def __init__(self, emailTemplate, emailFrom):
        self.emailTemplate = emailTemplate
        self.emailFrom = emailFrom

    def ParseData(full_path):
        try:
            full_path = re.sub(r'/', r'\\', full_path)
            hive = re.sub(r'\\.*$', '', full_path)
            if not hive:
                raise ValueError('Invalid \'full_path\' param.')
            if len(hive) <= 4:
                if hive == 'HKLM':
                    hive = 'HKEY_LOCAL_MACHINE'
                elif hive == 'HKCU':
                    hive = 'HKEY_CURRENT_USER'
                elif hive == 'HKCR':
                    hive = 'HKEY_CLASSES_ROOT'
                elif hive == 'HKU':
                    hive = 'HKEY_USERS'
            reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
            reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
            reg_value = re.sub(r'^.*\\', '', full_path)
            return hive, reg_key, reg_value
        except:
            return None, None, None

    def QueryValue(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)

            return {"isSuccess": True}
        except:
            return  {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

            


    def GetValue(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)

            return {
                "isSuccess": False,
                "message": value_of_value
            }
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

    def DecValue(c):
        c = c.upper()
        if ord('0') <= ord(c) and ord(c) <= ord('9'):
            return ord(c) - ord('0')
        if ord('A') <= ord(c) and ord(c) <= ord('F'):
            return ord(c) - ord('A') + 10
        return 0

    def str_to_bin(self, s):
        res = b""
        for i in range(0, len(s), 2):
            a = self.DecValue(s[i])
            b = self.DecValue(s[i + 1])
            res += (a * 16 + b).to_bytes(1, byteorder='big')
        return res

    def str_to_dec(self, s):
        s = s.upper()
        res = 0
        for i in range(0, len(s)):
            v = self.DecValue(s[i])
            res = res*16 + v
        return res


    def SetValue(self, full_path, value, value_type):
        value_list = self.ParseData(full_path)
        try:
            winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            if 'REG_BINARY' in value_type:
                if len(value) % 2 == 1:
                    value += '0'
                value = self.str_to_bin(value)
            if 'REG_DWORD' in value_type:
                if len(value) > 8:
                    value = value[:8]
                value = self.str_to_dec(value)
            if 'REG_QWORD' in value_type:
                if len(value) > 16:
                    value = value[:16]
                value = self.str_to_dec(value)                 
            
            winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
            winreg.CloseKey(opened_key)

            return {'isSuccess': True}
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }



    def DeleteValue(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            winreg.DeleteValue(opened_key, value_list[2])
            winreg.CloseKey(opened_key)
            
            return {'isSuccess': True}
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def QueryKey(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
            winreg.CloseKey(opened_key)

            return {'isSuccess': True}
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def CreateKey(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])

            return {'isSuccess': True}
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def DeleteKey(self, full_path):
        value_list = self.ParseData(full_path)
        try:
            winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])

            return {'isSuccess': True}
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

    def CreateRegistry(full_path):
        try:
            outout_file = os.getcwd() + '\\run.reg'
            with open(outout_file, 'w+') as f:
                f.write(full_path)
                f.close()
            os.system(r'regedit /s ' + os.getcwd() + '\\run.reg')
            return {
                "isSuccess": True,
                "message": "File reg created"
            }
        except:
            return {
                "isSuccess": False,
                "message": "Cannot create file reg"
            }

    def RegistryHandle(self):
        while True:
            time.sleep(5)
            requestContent = self.emailTemplate.Receive()
            if not requestContent:
                continue
            jsonContent = json.loads(requestContent)
            body = jsonContent["Body"]
            bodyJson = json.loads(body)
            data = bodyJson["Data"]

            ID = data['ID']
            full_path = data['path'] 
            name_value = data['name_value']
            value = data['value']
            v_type = data['v_type']

            if ID == -1:
                return
            
            elif ID == 0:
                response = self.CreateRegistry(full_path)

            elif ID == 1:
                response = self.GetValue(full_path + r'\\' + name_value)     

            elif ID == 2:
                response = self.SetValue(full_path + r'\\' + name_value, value, v_type)       

            elif ID == 3:
                response = self.CreateKey(full_path)

            elif ID == 4:
                response = self.DeleteKey(full_path + r'\\')
            
            self.emailTemplate.SendNotification(emailFrom = self.emailTemplate.userName , emailTo = self.emailFrom, subject = "[No-reply] Server Response", body = json.dumps(response))
        