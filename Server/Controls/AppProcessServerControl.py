import os
import psutil

class AppProcessServerControl:

    @staticmethod
    def ListApps():
        cmd = 'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
        proc = os.popen(cmd).read()
        return proc
        
    @staticmethod
    def ListProcesses():
        ls = 'Name\tID\tThreads\n----\t--\t-------\n\n'
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object. 
                name = proc.name()
                pid = proc.pid
                threads = proc.num_threads()
                ls += str(name) + '\t' + str(pid) + '\t' + str(threads) + '\n'
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return ls

    @staticmethod
    def Kill(taskID):
        command = 'taskkill.exe /F /PID ' + str(taskID)
        try:
            a = os.system(command)
            if a == 0:
                return {
                    'isSuccess': True,
                    "message": "Deleted task " + taskID
                }
            else:
                return {
                    "isSuccess": False,
                    "message": "Failed to process from the server. Please try one more time."
                }
        except:
            return {
                "isSuccess": False,
                "message": "Failed to process from the server. Please try one more time."
            }

    @staticmethod
    def LoadData(data):
        global action
        global ID
        global status

        action = '' 
        ID = -1
        status = ''

        if("Action" in data):
            action = data["Action"]
        if("ID" in data):
            ID = data["ID"]
        if("Status" in data):
            status = data["Status"]

    @staticmethod
    def Handle(data):
        try:
            AppProcessServerControl.LoadData(data)
            if "KILL" in action:
                return AppProcessServerControl.Kill(ID)
            elif "SHOW" in action:
                if "PROCESS" == status:
                    return AppProcessServerControl.ListProcesses()
                else:
                    return AppProcessServerControl.ListApps() 
        except:
            return {
                    "isSuccess": False,
                    "message":  "Failed to process from the server. Please try one more time."
                }