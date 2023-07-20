# gets csv file name
# returns: 1) tab tag (a16,a134)
#           2) list of fields for table creation
def getTabProperties(csvFilePath):
  import csv
  csv_filename = csvFilePath
  list_of_rows = []
  tabName= "empty"
  fieldList=["empty",]
  with open(csv_filename) as csv_file:
    row_count = 0

    csv_reader = csv.reader(csv_file, delimiter=',')
    k=0
    for row in csv_reader:
            k=k+1
            # adding the first row
            list_of_rows.append(row)

            # breaking the loop after the
            # first iteration itself
  if len(list_of_rows)==2    :
      fieldList =list_of_rows[0]
      valsList = list_of_rows[1]
      n1= len(fieldList)
      n2= len(valsList)
      if n1>2 and n2==n1:
        fieldList.pop(0)  # revove 2 first: tabTag and date
        fieldList.pop(0)


        tabName= valsList [0]
      else:
          print ("the data file is not in standard form")
          print("fields=",n1," values=",n2)
  else:
    print("the data file is not in standard form. only 2 lines allowed")

  return tabName,fieldList
