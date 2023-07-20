import pyodbc
print ("hello")


cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=192.168.203.61,1433\\SQLEXPRESS;"
                     "Database=agr-dcontrol;"
                      'UID=agr;'
                      'PWD=23@@enviRo;'
                     "Trusted_Connection=no;")

cursor = cnxn.cursor()
d=cursor.execute('SELECT * FROM z48')
row = cursor.fetchone()
print (row)
s="192.168.203.61,1433\\SQLEXPRESS"
user= "agr"
psw='23@@enviRo'
c2=  pyodbc.connect(driver='{SQL Server Native Client 11.0}', server=s, database="agr-dcontrol", uid=user, pwd=psw)
cur2= c2.cursor()
f= cur2.execute('''SELECT TOP (10) [id]
      ,[datetime]
      ,[monWSk]
      ,[monWD]
      ,[monWDSTc]
      ,[monWSMaxk]
      ,[monT]
      ,[monRH]
      ,[monT12m]
      ,[monT10m]
      ,[monTs30m1]
      ,[monTs12m1]
      ,[monRAD]
      ,[monPREC10]
      ,[monBV]
  FROM [agr-dcontrol].[dbo].[a10] where id < 230625045 order by id desc ''')

row = cur2.fetchone()
print (row)
