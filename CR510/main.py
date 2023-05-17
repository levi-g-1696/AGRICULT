import os,datetime
from CR510.cr510toCR1000 import cr510toCR1000
from CR510.cr510tools import removeOld_V2
import shutil,glob
import string,random,time

##################################################

def moveFiles (sourceFolder,destFolder,arcfolder):

  file_names = os.listdir(sourceFolder)
  if len(file_names)== 0 : return
  for file_name in file_names:
    randomStr = ''.join(random.choices(string.digits + string.ascii_letters, k=5))
    newfile_name=file_name + "-" + randomStr
    path= os.path.join(sourceFolder, file_name)
    pathForDest= os.path.join(destFolder, newfile_name)
    pathForArc=os.path.join(arcfolder, newfile_name)
    if os.path.isfile(path):
      shutil.copy(path, pathForArc)
      shutil.move(path, pathForDest)

  return
############################################


if __name__ == '__main__':
    rootpath = r'D:\Campbell-CR510'
    TEMPPath = rootpath + "\\TEMP"
    rawDataPath = rootpath + "\\Raw Data Files"
    shortArcPath = rootpath + "\\Short Arc"
    cr510StationsData = rootpath + "\\CR510 StationsData"
    lastOperationFile= rootpath+ "\\lastOperation.log"
    ##-----------------------------------
    # newStationPrompt()
    # -------------------------------
    for n in range(1,59):
      rawDataFolderslist = os.listdir(rawDataPath)
      for item in rawDataFolderslist:
        path = os.path.join(rawDataPath, item)
        if os.path.isdir(path):
            folder = item
            destFolder = os.path.join(TEMPPath, folder)
            arcFolder = os.path.join(shortArcPath, folder)
            moveFiles(path, destFolder, arcFolder)
        #  moveFiles(sourcePath,"destFolder")
      foldersInTemp = os.listdir(TEMPPath)
      for folder in foldersInTemp:
        path = os.path.join(TEMPPath, folder)
        files = os.listdir(path)
        for file in files:
            filePath = os.path.join(path, file)
            stationname = folder
            destFolder = os.path.join(cr510StationsData, folder)
            sourceRawDataFile = filePath
            cr510toCR1000(stationname, sourceRawDataFile, destFolder)
            os.remove(sourceRawDataFile)
      pathForRemove = shortArcPath + "\\*\\*"
      files = glob.glob(pathForRemove)
      minutesLimit = 2000
      deletedNum = removeOld_V2(files, minutesLimit)  # files,minuteLimit
      now = datetime.datetime.now()
      f = open(lastOperationFile, "w")
      f.write("the last operation of the script was :"+ str(now))
      f.close()
      time.sleep(60)
