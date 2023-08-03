import datetime
import time

import pyodbc
from datetime import datetime,timedelta
from csvValidations import getMonListFromDB,getTabNamesFromStationsTable,getTabNamesFrobDB
from fillDefaults import getLastTimeOfTab
from fillDefaults import makeTimeGridToTables
from csvValidations import getTabProperties
###############################
# one time tool to fill all existing tables to station table
# think it must contain station names only(a3,a45) not tha validations tables (a3v,a45v)
def addNewStations():
    #tool analises the tables that exist in db and write them to table
    #"stations. one time tool"
    qlist=[]
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    tabnames=getTabNamesFrobDB()
    for tname in tabnames:
      monlist= getMonListFromDB(tname)
      monlist.pop(0)
      monlist.pop(0)
      monListStr=""
      for i in range(0,len(monlist)):
          monListStr=monListStr + monlist[i]+";"
      monListStr= monListStr[:-1] #delete last ";"

      query= "INSERT INTO [dbo].[stations] ([tag] ,[monitors] ,[enable] )  VALUES "
      query =query + f"('{tname}','{monListStr}',1)"
      try:
          print("exequte sql query:\n", query)
          cursor.execute(query)
      except pyodbc.OperationalError as msg:
          print("Command skipped: ", msg)
    cursor.commit()
    cnxn.close()
    ###################################################
def addOneStation(tab):
    # a tool to add astation to table "stations"
        qlist = []
        cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                              "Database=agr-dcontrol;"
                              "Trusted_Connection=yes;")
        cursor = cnxn.cursor()
        tabnames = getTabNamesFrobDB()
        inp=""
        if tab in tabnames:
            inp=input (f"station {tab} was succesfully found in DB \n do you need to add it to stations table? y/n")
        if "y" in inp or "Y" in inp:
            print (f"{tab} will be just added")
            monlist = getMonListFromDB(tab)
            monlist.pop(0)
            monlist.pop(0)
            monListStr = ""
            for i in range(0, len(monlist)):
                monListStr = monListStr + monlist[i] + ";"
            monListStr = monListStr[:-1]  # delete last ";"

            query = "INSERT INTO [dbo].[stations] ([tag] ,[monitors] ,[enable] )  VALUES "
            query = query + f"('{tab}','{monListStr}',1)"
            try:
                print("exequte sql query:\n", query)
                cursor.execute(query)
            except pyodbc.OperationalError as msg:
                print("Command skipped: ", msg)
        else: print("No? ok. Good by.")
        cursor.commit()
        cnxn.close()
        ###################################################
    ############################################################
def addMonToScripts(monlist):
    qlist=[]
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()

    for monitor in monlist:

      monListStr=""


      query= "INSERT INTO [dbo].[MonToVldScript] ([mon] ,[type] ) VALUES "
      query =query + f"('{monitor}',1)"
      try:
          print("exequte sql query:\n", query)
          cursor.execute(query)
      except pyodbc.OperationalError as msg:
          print("Command skipped: ", msg)
    cursor.commit()
    cnxn.close()
    ###################################################
def addNewTableByDataFile(filePath)    :
         import os
         from sqlCreateTables import createTable
         from datetime import datetime,timedelta
         from dbFillRun import  fillFileValsToDB,isFileInGrid
         fpath= filePath
         if os.path.isfile(fpath):
           name,mlist= getTabProperties(fpath)
           if name=="empty":
               print ("addNewTableByDataFile says: file error")
               return
           elif name not in getTabNamesFrobDB():
              inp = input  (f"table name {name} was found in the file. \nDo you want to crate tables and grid for it (y/n)?\n")
              if "Y" in inp or "y" in inp :
                createTable(name,mlist)
                delta = timedelta(days=5)
                now = datetime.now()
                startgrid = now - delta
                makeTimeGridToTables(name,startgrid,7)
                print (f"tables for {name} and grid were succesfully created")
                addOneStation(name)

                os.rename(fpath,fpath+".used")
              else: print ("your answer was not 'y' \nBye")
           else: print (f"the name {name} already exist in db")
         else: print("the path is not a file.\nBye")
         return
############################################
def getCommonMonList():
    monset = set()
    tablist = getTabNamesFrobDB()
    tablist.remove('VLDstat')
    tablist.remove('stations')
    tablist.remove('MonToVldScript')
    tablist.remove('vldScripts')
    for tb in tablist:
        monlist = getMonListFromDB(tb)
        monlist.pop(0)
        monlist.pop(0)
        """if "mVT" in monlist:
            print("mVT in tab ",tb)
        if "mRS" in monlist:
            print("mRS in tab ", tb)"""
   #     print(tb, "## ", monlist)
       # monset.update(monlist)
        monset |= set(monlist)
   # print(monset)
   # print(len(monset))
    return list(monset)

ml= getCommonMonList()
monTag="monWD222"
#if monTag not in ml: print (f"monTag {monTag} is not in use in the DB")
#else : print(f"monTag {monTag} is already in use ")
filepath=r"D:\csv for new station sreating\pen114.fromLSI-20230716.1012-FKDrg.csv"

addNewTableByDataFile(filepath)
##name="43a10"
# delta = timedelta(days=5)
# now = datetime.now()
# startgrid = now - delta
# makeTimeGridToTables("43a10",startgrid,7)
# print (f"tables for {name} and grid were succesfully created")
# addOneStation(name)
