import datetime
import time

import pyodbc

from csvValidations import getMonListFromDB,getTabNamesFromStationsTable,getTabNamesFrobDB
from fillDefaults import getLastTimeOfTab
from fill2 import makeTimeGridToTables
from csvValidations import getTabProperties
###############################
# one time tool to fill all existing tables to station table
# think it must contain station names only(a3,a45) not tha validations tables (a3v,a45v)
def addNewStations():
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
#addMonToScripts(ml)