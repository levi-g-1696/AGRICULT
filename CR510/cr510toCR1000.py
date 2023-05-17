import csv,random,string
from datetime import datetime, timedelta
def makeFile10m(stname,destfileFolder,list10m_of_rows) :

    # create file if need
    if len(list10m_of_rows)== 0 :return
    firstrow = list10m_of_rows[0]
    days = int(firstrow[2])
    hour = int(firstrow[3]) // 100
    min = int(firstrow[3]) - hour * 100
    year = int(firstrow[1])
    d = datetime(year, 1, 1, hour, min) + timedelta(days - 1)
    destfile = makeFileName(stname, destfileFolder, d)
    headline=f'"fileFromScript","{stname} CR10..510","Min10"'
    line2 = '"TMSTAMP","RECNBR=1","data_columns"'
    with open(destfile, "a") as myfile:
        myfile.write(headline+"\n")
        myfile.write(line2+"\n")

    # write date lines to file
    for row in list10m_of_rows:
      days= int(row[2])
      hour= int(row[3])//100
      min= int(row[3])-hour*100
      year = int(row[1])
      d = datetime(year, 1, 1, hour, min) + timedelta(days - 1)

      timestamp='"'+d.strftime("%Y-%m-%d %H:%M:%S")+'"'
      lineData=timestamp+ ",1"
      for fieldNum in  range(4, len(row)):
          lineData= lineData + ","+ row[fieldNum]
      #print ("linedata:",lineData)
      with open(destfile, "a") as myfile:
        myfile.write(lineData+"\n")
    return
def    makeFile24h (destfile,list10m_of_rows) :
    return
def makeFileName(stationName,destFolder,datetime):
    zeroChar=""
    if (datetime.month <10): zeroChar="0"
    fullFilePath= destFolder +"\\" + stationName +"."+ str(datetime.year)+ zeroChar +str(datetime.month)+ str(datetime.day)+"."+ str(datetime.hour) + str(datetime.minute)
    randomStr=''.join(random.choices(string.digits+string.ascii_letters, k=5))
    fullFilePath = fullFilePath + "-"+randomStr+ ".dat"
    return fullFilePath

def cr510toCR1000(stationName, sourceFile,destFolder):

  csv_filename=sourceFile

# move file to tempfolder
  list10m_of_rows=[]
  list24h_of_rows=[]
  code10m="110"
  code24h="124"
  with open(csv_filename) as csv_file:
    row_count = 0

    csv_reader = csv.reader(csv_file, delimiter=',')
    k = 0

    line_count = 0
    for row in csv_reader:
        if row[0]==code10m:
          list10m_of_rows.append(row)
        elif row[0] == code24h:
            list24h_of_rows.append(row)

    makeFile10m(stationName,destFolder,list10m_of_rows)
   # makeFile24h (destfile,list10m_of_rows)
