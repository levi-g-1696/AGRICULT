import datetime
import time

import pyodbc

from csvValidations import getTabProperties,getMonListFromDB,getTabNamesFromStationsTable
from fillDefaults import getLastTimeOfTab
from fill2 import makeTimeGridToTables
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



prepareTablesGrid()