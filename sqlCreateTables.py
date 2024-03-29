import pyodbc
outFile= ".\\datafiles\\newStationCreationScript.txt"
######################################
def writeLine(file,line):
  with open(file, 'a') as the_file:
    the_file.write(line +"\n")

###########################################
def createTable(tabName,columnsList):
  cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-3BJPAFM\\SQLEXPRESS;"
                      "Database=agr-dcontrol;"
                      "Trusted_Connection=yes;")


  cursor = cnxn.cursor()

  prefxString= '''CREATE TABLE [dbo].['''

  columnNames=["monX1","monX2","monX3"]
  pkStringRT= "[PK_"+tabName+ "]"
  pkStringVLD = "[PK_" + tabName +"_vld" + "]"

  loopStrRT=''
  loopStrVLD=''
  for col in columnsList:
    loopStrRT=loopStrRT+ '[' +col +'] [real] NULL,'
    loopStrVLD=loopStrVLD + '[' +col +'] [varchar](30) NULL,'
#  meadlSttring1='''](	[id] [bigint] IDENTITY(1,1) NOT NULL,[datetime] [datetime] NULL,'''
  meadlSttring1 = '''](	[id] [bigint] NOT NULL,[datetime] [datetime] NULL,'''
  postStringRT= '  CONSTRAINT '+ pkStringRT  + ' PRIMARY KEY CLUSTERED ' +  '''
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

'''
  postStringVLD = '  CONSTRAINT ' + pkStringVLD + ' PRIMARY KEY CLUSTERED ' + '''
  (
  	[id] ASC
  )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
  ) ON [PRIMARY];

  '''
  scriptRT= prefxString +tabName + meadlSttring1 +loopStrRT+ postStringRT
  scriptVLD=prefxString +tabName +"v" + meadlSttring1 +loopStrVLD + postStringVLD
  print ("runing create tableRT for ", tabName)


#comandlist= script.split(';')

  cursor.execute(scriptRT)
  writeLine(outFile,scriptRT)
  cnxn.commit()
  print("runing create tableVLD for ", tabName)
  cursor.execute(scriptVLD)
  writeLine(outFile,scriptVLD)
  cnxn.commit()
  return
#print (comandlist)
