import csv
import datetime
import os
import shutil
from datetime import timedelta

import pyodbc
from dateutil import parser
from dateutil.parser import parse

import globalConfig
from csvValidations import checkFileCommon
from dbFillRun import download20Ftp
from getTabProps import getTabProperties

##################################################
def getNext10mTime(dt):
    #______________________________
    def roundDate(dt):
        discard = timedelta(minutes=dt.minute % 10,
                            seconds=dt.second,
                            microseconds=dt.microsecond)
        dt -= discard
        if discard >= timedelta(minutes=5):
            dt += timedelta(minutes=10)
        return dt
    #__________________________________________
    delta10m = timedelta(minutes=10)
    nextdate = dt+ delta10m
    return roundDate(nextdate)

################################################################

############################################
def makeTimeGridToTables(tabName,fromDate,daysNum):
  statusTable="VLDstat"
  #lastTime = getLastTimeOfTab(tabName)

  #dt = datetime.now()
  dt = fromDate
  delta10days= timedelta(days=daysNum)

  enddate= dt+delta10days

  cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                      "Database=########agr-dcontrol;"
                      "Trusted_Connection=yes;")

  cursor = cnxn.cursor()
  tabVLDname= tabName+"v"

  nextdate= getNext10mTime(fromDate)
  datastateDef=-10
  sendstateDef=0
  vldstateDef=0
  while (nextdate< enddate):
    nextid= getIDbyTime(nextdate)

    if isIDinDBgrid(tabName,nextid):
      nooperation=1
    #  print(f"makeTimeGridToTables says: id {nextid} already in table {tabName} ")

    else :
        dateStr = nextdate.strftime("%Y-%m-%dT%H:%M:%S")
        com = f"INSERT INTO [{tabName}] (id,datetime) VALUES ({nextid},'{dateStr}')"
        comVLD = f"INSERT INTO [{tabVLDname}] (id,datetime) VALUES ({nextid},'{dateStr}')"
        comStatus = f"INSERT INTO [{statusTable}] (tableName,FK,datastate,vldstate,sendstate) VALUES ( '{tabName}',{nextid},{datastateDef},{vldstateDef},{sendstateDef})"
        print(com)
        cursor.execute(com)
        cursor.execute(comVLD)
        print(comStatus)
        cursor.execute(comStatus)
    nextdate = getNext10mTime(nextdate)
  cursor.commit()

#################################################

def getIDbyTime(dt):
# dt is datetime type

  y= dt.year-2000
  m= dt.month
  d= dt.day
  h=dt.hour
  min= dt.minute
  id= int ( y* 10000000 + m * 100000 + d*1000 + h*10 + min/10)
  return id

###################################################################
def isIDinDBgrid(tabName,id):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    checkIfExistCom = f"select id from [{tabName}] where id= {id}"
    cursor.execute(checkIfExistCom)

    row = cursor.fetchone()

    if row == None or row[0] == None:
        print(f"id {id} for {tabName} is not in grid")
        return False
    else:
        print(f"new id {id} for {tabName}  is in grid!!")
        return True
##############################################################

############################################
def isFileInGrid(csvFile):
    #___________________________________________
    def getDate(csvRow):
        dateColumnNum = 1
        nextDate = csvRow[dateColumnNum]
        #   parse(nextDate)
        return parse(nextDate)
    #__________________________________________
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
##############################################
def dbFillRun():
    csvFolder = globalConfig.csvFilesDirectory

    delta = timedelta(days=5)
    now = datetime.now()
    startgrid = now - delta
    ip = "192.168.203.45"
    port = "21"
    user = "dcontrol10m"
    psw = "23d-CONTROL"

    out = r"D:\loggernet CSV files\not in grid"
    userForSendDBStruct = "dbstruct"
  #  getFilelistFTP(ip, port, user, psw)

    pathlist = download20Ftp(csvFolder, ip, port, user, psw)
    ftpFolderIsNotEmpty= len(pathlist)>0
    while ftpFolderIsNotEmpty:
       for fpath in pathlist: #>>>>>>>>>>>>>>>>>>
          if os.path.isfile(fpath):
            validationOK,errorCode=checkFileCommon(fpath)
            print ("dbfillRun.validation step.val=",validationOK)
            if validationOK:
                shutil.copy(fpath,globalConfig.arcOkDirectory)
                if not isFileInGrid(fpath):
                    delta6h = timedelta(hours=6)
                    dtFrom = datetime.now() - delta6h
                    name, mlist = getTabProperties(fpath)
                    makeTimeGridToTables(name, dtFrom, 0.5)
                fillFileValsToDB(fpath)
            else:
                shutil.copy(fpath,globalConfig.arcError)
                logfileStructError(fpath,errorCode)
            os.remove(fpath)
        #end for

       pathlist = download20Ftp(csvFolder, ip, port, user, psw)
       ftpFolderIsNotEmpty = len(pathlist) > 0
    #END WHILE
    print("the main of dbfillRun says:ftpFolderIsNotEmpty = ",ftpFolderIsNotEmpty )
    prepareTablesGrid()
    #################################################################