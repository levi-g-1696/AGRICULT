from datetime import datetime
import json,os
import time
from dbFillRun import dbFillRun
statusFile=".\\runStatusForDBFILL.json"
##############################################################
def setRunFlagON():
    with open(statusFile, 'r') as f:
        json_data = json.load(f)
    json_data["runFlag"] = 'run'  # On this line you needed to add ['embed'][0]
    with open(statusFile, 'w') as f:
        json.dump(json_data, f,indent=2)
 ##################################################################
def setLastRunTime():
    with open(statusFile, 'r') as f:
        json_data = json.load(f)
    date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
    json_data["lastRunTime"] = date_string # On this line you needed to add ['embed'][0]
    with open(statusFile, 'w') as f:
        json.dump(json_data, f, indent=2)
 #########################################
def getRunFlag():

    with open(statusFile, 'r') as f:
        json_data = json.load(f)
        if json_data["runFlag"] == 'run':
              return True
        else:return False
        ############################################################
def setRunFlagOFF():
    import json
    statusFile = ".\\runStatusForDBFILL.json"
    with open(statusFile, 'r') as f:
        json_data = json.load(f)
    json_data["runFlag"] = 'stop'  # On this line you needed to add ['embed'][0]
    with open(statusFile, 'w') as f:
        json.dump(json_data, f,indent=2)
        ###########################################################################


if __name__ == '__main__':
    os.chdir(r"C:\Users\office22\PycharmProjects\agricult")
    setRunFlagON()
    while getRunFlag():
     #tool must be here
      dbFillRun()
      dt= datetime.now()
      setLastRunTime()
      print(f"{dt}  tool is running.\n ")
      time.sleep(20)