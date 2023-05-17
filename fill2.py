from fillDefaults import getIDbyTime
import csv
from dateutil.parser import parse
def getDate(csvRow):
    dateColumnNum=1
    nextDate=csvRow[dateColumnNum]
    parse(nextDate)
    return parse(nextDate)
def buildSqlReq(tabname,monList,csvRow):
    time= getDate(csvRow)
    id= getIDbyTime(time)

    csvRow.pop(0)
    csvRow.pop(0)
    valList= csvRow
    str= f"UPDATE {tabname} set "
    str = str + monList[0] + "=" + valList[0]
    if len(monList>1):
      for i in range(1,len(monList)):
        str= str+ ", "+monList[i] +"="+ valList[i]
    str= str+ f" WHERE id={id}"
