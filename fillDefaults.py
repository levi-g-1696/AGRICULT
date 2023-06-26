import pyodbc
from datetime import datetime, timedelta

def roundDate(dt):

    discard = timedelta(minutes=dt.minute % 10,
                        seconds=dt.second,
                        microseconds=dt.microsecond)
    dt -= discard
    if discard >= timedelta(minutes=5):
        dt += timedelta(minutes=10)
    return dt
###############################################################


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
def getLastTimeOfTab(tabName):
  cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-5CJPAFM\\SQLEXPRESS;"
                      "Database=agr-dcontrol;"
                      "Trusted_Connection=yes;")

  cursor = cnxn.cursor()
  #^^^^^^^^^^^^^^^^^^^^debug^^^^^^^^^^^^^^^^^^^^
  #d = cursor.execute(f'SELECT datetime FROM {tabName}')
 # row = cursor.fetchone()
#  print(row)
  #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  dt = datetime.now()
  deltadays = timedelta(days=2)
  try:
    com=f'SELECT  max(datetime)  FROM [{tabName}]';
   # print (com)
    cursor.execute(com)
    row = cursor.fetchone()
    if row == None or row[0] == None: #table is empty
        dt = dt - timedelta(hours=12)

    else:   #table has entries
    #   print (row,"debug6556")
       dt = roundDate(row[0]) -timedelta(hours=0.2)
 #
  except:
    print ("getLastTimeOfTab says:exception on connecting to db or time parsing")

  dt = roundDate(dt)

  return dt

################################################################
def isIDinDBgrid(tabName,id):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-5CJPAFM\\SQLEXPRESS;"
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
##################################################
def getNext10mTime(dt):
    delta10m = timedelta(minutes=10)
    nextdate = dt+ delta10m
    return roundDate(nextdate)

################################################################
def makeTimeGridToTables(tabName,fromDate,daysNum):
  statusTable="VLDstat"
  #lastTime = getLastTimeOfTab(tabName)

  #dt = datetime.now()
  dt = fromDate
  delta10days= timedelta(days=daysNum)

  enddate= dt+delta10days

  cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=DESKTOP-5CJPAFM\\SQLEXPRESS;"
                      "Database=agr-dcontrol;"
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


#makeTimeGridToTables(("z49"))
