import os,datetime
import shutil,glob
import string,random

##################################################################
def newStationPrompt():
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)

    if not os.path.exists(TEMPPath):
        os.makedirs(TEMPPath)

    if not os.path.exists(rawDataPath):
        os.makedirs(rawDataPath)
    newStation = input("input new CR510 station name. The necessery folders will be created:\n")
    if newStation == "":
        print("new station input is canceled")

    else:
        confirm = input(f"new station name will be:{newStation} (y/n)\n")
        if confirm.upper() == "Y":
            createnew(newStation)
        else:
            print("\n your answer was  " + confirm + "\n new station was not created")
   ###############################################################

def createnew(stationName):
    newpath= rootpath+"\\" +stationName
    TEMPPath = rootpath + "\\TEMP" +"\\" +stationName
    rawDataPath = rootpath + "\\Raw Data Files"+ "\\" +stationName
    shortArcPath = rootpath + "\\Short Arc"+ "\\" +stationName
    cr510StationsData = rootpath + "\\CR510 StationsData"+ "\\" +stationName

    if not os.path.exists(cr510StationsData):
      os.makedirs(cr510StationsData)
      if not os.path.exists(TEMPPath):
            os.makedirs(TEMPPath)
      if not os.path.exists(rawDataPath):
            os.makedirs(rawDataPath)
      if not os.path.exists(shortArcPath):
          os.makedirs(shortArcPath)
    else: print (f"station {stationName} already exist ")
    return

##################################################


rootpath = r'D:\Campbell-CR510'
TEMPPath= rootpath + "\\TEMP"
rawDataPath= rootpath + "\\Raw Data Files"
shortArcPath=rootpath +"\\Short Arc"
cr510StationsData= rootpath +"\\CR510 StationsData"


for i in range(5):
    newStationPrompt()
##-----------------------------------
#newStationPrompt()
#-------------------------------
