import pyodbc
print ("hello")
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                     "Database=agr-dcontrol;"
                     "Trusted_Connection=yes;")

cursor = cnxn.cursor()
d=cursor.execute('SELECT * FROM z48')
row = cursor.fetchone()
print (row)