import csv
from datetime import datetime
from ftplib import FTP
import os
from fill2 import  getDate
import pyodbc
from fillDefaults import getIDbyTime
from getTabProps import getTabProperties


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


def download20Ftp(workFolder,ip,port,user,psw):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    files = []
    filenames = ftp.nlst()  # get filenames within the directory

    n=20
    for filename in filenames:
        local_filename = os.path.join(workFolder, filename)
        print(local_filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)

        file.close()
        try:
            ftp.delete(filename)
            print("file was deletd:",filename)
        except Exception:
            ftp.rmd(filename)
        n=n-1
        if n==0 :break
    ftp.quit()  #
def isIDinDBgrid(tabName,id):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                          "Database=agr-dcontrol;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    checkIfExistCom = f"select id from [{tabName}] where id= {id}"
    print (checkIfExistCom)
    cursor.execute(checkIfExistCom)

    row = cursor.fetchone()

    if row == None or row[0] == None: return False
    else: return True
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
                    break

            line_count += 1
        return result
ip= "192.168.201.45"
port= "21"
user = "dcontrol10m"
psw= "23d-CONTROL"
wdir= r"C:\Users\office22\Desktop\zmani\ftp"

file= r"C:\Users\office22\Desktop\zmani\ftp\1.H180520230550_180520230550.scv"
n1= datetime.now()
r=isFileInGrid(file)
n2= datetime.now()
n3= n2-n1

print (r)
print(n3)
