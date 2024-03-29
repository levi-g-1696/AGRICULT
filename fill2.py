import os
import shutil

from fillDefaults import makeTimeGridToTables,isIDinDBgrid
#makeTimeGridToTables(tabName,fromDate,daysNum):
import pyodbc
from csvValidations import getTabNamesFrobDB
import globalConfig
from sqlCreateTables import createTable
from csvValidations import checkFileCommon,makeDbPropsInCsv
from fillDefaults import getIDbyTime
import csv
from ftplib import FTP
from datetime import datetime,timedelta
from dateutil.parser import parse
from getTabProps import getTabProperties
from mylogging import logDataFillError

##############################################################
def getDate(csvRow):
    dateColumnNum=1
    nextDate=csvRow[dateColumnNum]
    parse(nextDate)
    return parse(nextDate)
############################################
def buildSqlReq(tabname,monList,csvRow):
    time= getDate(csvRow)
    id= getIDbyTime(time)

    csvRow.pop(0)
    csvRow.pop(0)
    valList= csvRow
    str= f"UPDATE [{tabname}] set "
    str = str + monList[0] + "=" + valList[0]
    if len(monList)>1:
      for i in range(1,len(monList)):
        str= str+ ", "+monList[i] +"="+ valList[i]
    str= str+ f" WHERE id={id}"
    return str
###################################################
def fillFileValsToDB(csvFile):
  valsList=[]
  reqList=[]
  tabName,monList = getTabProperties(csvFile)
  with open(csvFile) as csv_file:
        row_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        k = 0
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
           #go to next- only data lines we need
                line_count += 1
            else :
                req= buildSqlReq(tabName,monList, row)
                reqList.append(req)
            line_count += 1
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                              "Database=agr-dcontrol;"
                              "Trusted_Connection=yes;")
        cursor = cnxn.cursor()
        for req in reqList:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
          try:
            print("exequte sql query:\n", req)
            cursor.execute(req)
          except pyodbc.OperationalError as msg:
            print("Command skipped: ", msg)
        cursor.commit()
        cnxn.close()
 ##########################################################################
def dbFiller(csvFileList)  :

    for filePath in csvFileList:
        isFileStructOK,errorCode= checkFileCommon(filePath)
        if isFileStructOK :
            fillFileValsToDB(filePath)
        else:logDataFillError(filePath,errorCode)

############################################################################

def getFilelistFTP(ip,port,user, psw):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    files = []

    try:
        files = ftp.nlst()
    except ftp.error_perm as resp:
        if str(resp) == "550 No files found":
            print
            "No files in this directory"
        else:
            raise
    n=50
    for f in files:
        print (f)
        n=n-1
        if n==0: break
    ftp.close()
    return
#######################################################################

def download20Ftp(workFolder,ip,port,user,psw):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    files = []
    filenames = ftp.nlst()  # get filenames within the directory

    counter=20
    for filename in filenames:
        local_filename = os.path.join(workFolder, filename)
        print(local_filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)

        file.close()
        try:
            ftp.delete(filename)
            print("FTP. file was deletd:",filename)
        except Exception:
            ftp.rmd(filename)
        counter=counter-1
        if counter==0 :break
    ftp.quit()
    ftp.close()
    fullpathList=[]
    fileList = os.listdir(workFolder)
    for f in fileList:
        fpath = os.path.join(csvFolder, f)
        fullpathList.append(fpath)
    #
    return fullpathList
######################################################################
def push_file_FTP(ip,port,user, psw,filePath):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    fileNameStrArr=str(filePath).split("\\")
    lastIndx= len(fileNameStrArr)-1
    fileName= fileNameStrArr[lastIndx]

    ftp.storbinary('STOR ' + fileName, open(filePath, 'rb'))
    ftp.close()
################################################
def isFileInGrid(csvFile):
    with open(csvFile) as csv_file:
        row_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        k = 0
        line_count = 0
        result= True
        for row in csv_reader:
            if line_count == 0:
                # go to next- only data lines we need
                line_count += 1
            else:
                dt=getDate(row)

                rowid= getIDbyTime(dt)
                tname,x= getTabProperties(csvFile)
                if isIDinDBgrid(tname,rowid) :continue
                else:
                    result=False
                   # print (f"isFileIngrid says: file {csvFile} tab {tname} has not grid in Db for {rowid}")
                    break

            line_count += 1
        return result
#################################################
csvFolder= globalConfig.csvFilesDirectory

delta=  timedelta(days=5)
now = datetime.now()
startgrid= now - delta
ip= "192.168.203.45"
port= "21"
user = "dcontrol10m"
psw= "23d-CONTROL"
csvFolder= r"D:\loggernet CSV files"
out=r"D:\loggernet CSV files\not in grid"
userForSendDBStruct="dbstruct"
getFilelistFTP(ip,port,user,psw)
#1000 files
# for i in range (300):
#   pathlist = download20Ftp(csvFolder, ip, port, user, psw)
#
#   for fpath in pathlist:
#     if os.path.isfile(fpath):
#       name,mlist= getTabProperties(fpath)
#       if name not in getTabNamesFrobDB():
#          createTable(name,mlist)
#          makeTimeGridToTables(name,startgrid,7)
#       if isFileInGrid(fpath)  :  fillFileValsToDB(fpath)
#       else:
#       #  shutil.copy(fpath,out)
#         delta6h = timedelta(hours=6)
#         dtFrom = datetime.now() - delta6h
#         dtTo = datetime.now() + delta6h
#         makeTimeGridToTables(name, dtTo, 0.5)
#         fillFileValsToDB(fpath)
#       os.remove(fpath)
#
#   file=r"C:\Users\office22\PycharmProjects\agricult\datafiles\dbStruct.csv"
#   makeDbPropsInCsv(file)
#   push_file_FTP(ip,port,userForSendDBStruct,psw,file)