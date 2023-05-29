
import csv, pyodbc
from getTabProps import  getTabProperties
from dateutil.parser import parse
#######################################################################
def check_empty_fields2(csv_filename): # without gui
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
    return isok
#####################################################################

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
    return result
#################################################################
def getMonListFromDB(tabName):
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
    return result

  ##############################################################
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

  ####################################################################################################
def checkFileCommon(csv_filename): # without gui
   tabName,monitorList = getTabProperties(csv_filename)
   tabNamesFromDB=getTabNamesFrobDB()
   tabNameErr= tabName not in tabNamesFromDB

   monListFromDb= getMonListFromDB(tabName)
   monListErr= False
   for item in monitorList:
       if item not in monListFromDb:
           monListErr= True
           break

  # monListErr=when not all in monitorList are in monListFromDb
  # print ("monlist err from checkFileCommon:",monListErr)
   dateOK= checkDateField(csv_filename)
  # print (tabNameErr)
   checkOK= not monListErr and not tabNameErr and dateOK
   errorCode=tabNameErr*100+ (not dateOK)*10 +monListErr*2
   if errorCode >100 : errorCode= 100

   return checkOK,errorCode




#file= r"C:\Users\office22\Desktop\zmani\agricultCSV\a48.csv"
#print (checkFileCommon(file))





