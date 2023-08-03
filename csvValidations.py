
import csv, pyodbc
from getTabProps import  getTabProperties
from dateutil.parser import parse
#######################################################################
def check_browkenRows(csv_filename):  # checks rows without csv fields and multiple lines with the same date
    isok = True
    with open(csv_filename) as file_in:
        lines = []

        for line in file_in:
            lines.append(line)
        if len(lines) < 2: return False
        firstLineCommaCount = lines[0].count(",")
        firstdataLine = lines[1]
        firstdataLineList = firstdataLine.split(",")
        firstDatalineDate = firstdataLineList[1]

        for line in lines:

            if line.count(",") != firstLineCommaCount:
                return False
        if len(lines) > 2:
            for k in range(2, len(lines)):
                line = lines[k]
                nextdataLineList = line.split(",")
                nextDatalineDate = nextdataLineList[1]
                if firstDatalineDate == nextDatalineDate:
                    return False

    return isok


######################################################
####################################################################################################
def checkFileCommon(csv_filename):  # without gui
    tabName, monitorList = getTabProperties(csv_filename)
    tabNamesFromDB = getTabNamesFromStationsTable()

  #  print ("checkfilecommon says:tabName=",tabName,"\n tabnames from db= ",tabNamesFromDB)
    tabNameErr = tabName not in tabNamesFromDB
   # print ("tamname error=",tabNameErr)
    monListFromDb = getMonListFromDB(tabName)
    monListErr = False
    for item in monitorList:
        if item not in monListFromDb:
            monListErr = True
            break
    brokenLinesErr = not check_browkenRows(csv_filename)
    # monListErr=when not all in monitorList are in monListFromDb
    # print ("monlist err from checkFileCommon:",monListErr)
    dateOK = checkDateField(csv_filename)
    # print (tabNameErr)
    checkOK = not monListErr and not tabNameErr and dateOK and not brokenLinesErr
    errorCode = tabNameErr * 100 + (not dateOK) * 10 + monListErr * 2 + brokenLinesErr * 200
    if 100 < errorCode and errorCode < 200: errorCode = 100

    return checkOK, errorCode
############################################################################
"""def check_empty_fields2(csv_filename): # without gui
    isok=True


    with open(csv_filename) as csv_file:
        row_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if not row:
                isok = False

        row_count = 0
        csv_file.seek(0)
        for row in csv_reader:
            col_count = 0
            for col in row:
                if col == "":
                    isok=False
                    print("Found empty field at row: {}, col: {}".format(row_count, col_count))

                col_count += 1
            row_count += 1
    return isok    """
#####################################################################
def check_browkenRows(csv_filename):  # checks rows without csv fields and multiple lines with the same date
    isok = True
    with open(csv_filename) as file_in:
        lines = []

        for line in file_in:
            lines.append(line)
        if len(lines) < 2: return False
        firstLineCommaCount = lines[0].count(",")
        firstdataLine = lines[1]
        firstdataLineList = firstdataLine.split(",")
        firstDatalineDate = firstdataLineList[1]

        for line in lines:

            if line.count(",") != firstLineCommaCount:
                return False
        if len(lines) > 2:
            for k in range(2, len(lines)):
                line = lines[k]
                nextdataLineList = line.split(",")
                nextDatalineDate = nextdataLineList[1]
                if firstDatalineDate == nextDatalineDate:
                    return False

    return isok


######################################################
def checkDateField(csvFilePath):
    import csv
    csv_filename = csvFilePath
    dateColumnNum=1
    list_of_rows = []
    with open(csv_filename) as csv_file:
        row_count = 0

        csv_reader = csv.reader(csv_file, delimiter=',')
        k = 0

        line_count = 0
        for row in csv_reader:
            if line_count == 0:
           #go to next- only data lines we need
                line_count += 1
            else :list_of_rows.append(row)
            line_count += 1
    datelist=[]
    result=True
    for item in list_of_rows:
        nextDate=item[dateColumnNum]
        try:
            parse(nextDate)

        except ValueError:
             result = False
    return result
#############################################################################################################
def getTabNamesFrobDB():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    d = cursor.execute('SELECT name FROM sys.Tables')
    row = cursor.fetchall()
    result = []
    for t in row:
        result.append(t[0])
    cnxn.close()
    return result
#############################################################
def getTabNamesFromStationsTable():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    d = cursor.execute('SELECT tag FROM stations where enable = 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ')
    row = cursor.fetchall()
    result = []
    for t in row:
        result.append(t[0])
    #    break
    cnxn.close()
    return result
#################################################################
def getMonListFromDB(tabName):
   # print ("getmonlist says: trying connect to db.  table ",tabName)
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()

    d = cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='"+tabName +"'")
    row = cursor.fetchall()
    result = []
    for t in row:
        result.append(t[0])
    cnxn.close()
    return result
#####################################################################
def getCommonMonList(): # only for db building
    monset = set()
    tablist = getTabNamesFrobDB()
    tablist.remove('VLDstat')
    tablist.remove('stations')
    for tb in tablist:
        monlist = getMonListFromDB(tb)
        print(tb, "## ", monlist)
        monset.update(monlist)
        monset |= set(monlist)
    print(monset)
    print(len(monset))
    return list(monset)
#############################################################
def getMonListFromStationsTable(tabName):
   ## print ("getmonlist says: trying connect to db.  table ",tabName)
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    req= f"select monitors from [dbo].[stations] where tag='{tabName}'"
    cursor.execute(req)
    row = cursor.fetchone()
  #  print (row)
    monstring = row [0]

    monlist= monstring.split(";")
    return monlist

   # monlist.pop(0)
   # monlist.pop(0)
 #   cnxn.close()
   # return result


  ##############################################################

def makeDbPropsInCsv(filePath):
  with open(filePath, 'w') as file:
     file.write('table,monitors\n')
  with open(filePath, 'a') as file:
    tabnames=getTabNamesFrobDB()
    for tname in tabnames:
      monlist= getMonListFromDB(tname)
      monListStr=""
      for i in range(0,len(monlist)):
          monListStr=monListStr + monlist[i]+";"
      monListStr= monListStr[:-1] #delete last ";"
      row= tname +","+monListStr+"\n"
      file.write(row)

  ##################################################

  ####################################################################################################



#file= r"C:\Users\office22\Desktop\zmani\agricultCSV\a48.csv"
#print (checkFileCommon(file))
print (getTabNamesFromStationsTable())

f=r"D:\loggernet CSV files\tst\a38.fromLogntDAT-2023083.1612-St338.csv"
checkFileCommon(f)

