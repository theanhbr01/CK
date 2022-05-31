import re, winreg, json
import os
class RegistryControl:
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

    def QueryValue(full_path):
        value_list = ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)

            return {"isSuccess": True}
        except:
            return 
            {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

            


    def GetValue(full_path):
        value_list = ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)

            return 
            {
                "isSuccess": False,
                "message": value_of_value
            }
        except:
            return 
            {
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

    def str_to_bin(s):
        res = b""
        for i in range(0, len(s), 2):
            a = DecValue(s[i])
            b = DecValue(s[i + 1])
            res += (a * 16 + b).to_bytes(1, byteorder='big')
        return res

    def str_to_dec(s):
        s = s.upper()
        res = 0
        for i in range(0, len(s)):
            v = DecValue(s[i])
            res = res*16 + v
        return res


    def SetValue(full_path, value, value_type):
        value_list = ParseData(full_path)
        try:
            winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            if 'REG_BINARY' in value_type:
                if len(value) % 2 == 1:
                    value += '0'
                value = str_to_bin(value)
            if 'REG_DWORD' in value_type:
                if len(value) > 8:
                    value = value[:8]
                value = str_to_dec(value)
            if 'REG_QWORD' in value_type:
                if len(value) > 16:
                    value = value[:16]
                value = str_to_dec(value)                 
            
            winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
            winreg.CloseKey(opened_key)

            return {'isSuccess': True}
        except:
            return 
            {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }



    def DeleteValue(full_path):
        value_list = ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            winreg.DeleteValue(opened_key, value_list[2])
            winreg.CloseKey(opened_key)
            
            return {'isSuccess': True}
        except:
            return 
            {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def QueryKey(full_path):
        value_list = ParseData(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
            winreg.CloseKey(opened_key)

            return {'isSuccess': True}
        except:
            return 
            {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def CreateKey(full_path):
        value_list = ParseData(full_path)
        try:
            winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])

            return {'isSuccess': True}
        except:
            return 
            {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }


    def DeleteKey(full_path):
        value_list = ParseData(full_path)
        try:
            winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])

            return {'isSuccess': True}
        except:
            return 
            {
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
            return 
            {
                "isSuccess": True,
                "message": "File reg created"
            }
        except:
            return 
            {
                "isSuccess": False,
                "message": "Cannot create file reg"
            }
    
    def RegistryHandle(self, emailTemplate):
        while True:
            params = gmail.Receive()
            params = params.body

            msg = json.loads(params)
            # extract elements
            ID = msg['ID']
            full_path = msg['path'] 
            name_value = msg['name_value']
            value = msg['value']
            v_type = msg['v_type']
            if ID == -1:
                return
            
            elif ID == 0:
                response = CreateRegistry(full_path)

            elif ID == 1:
                response = GetValue(full_path + r'\\' + name_value)     

            elif ID == 2:
                response = SetValue(full_path + r'\\' + name_value, value, v_type)       

            elif ID == 3:
                response = CreateKey(full_path)

            elif ID == 4:
                response = DeleteKey(full_path + r'\\')
            
            emailTemplate.SendNotification(emailFrom = emailTemplate.username, emailReplyTo)
        