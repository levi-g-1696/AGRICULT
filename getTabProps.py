# gets csv file name
# returns: 1) tab tag (a16,a134)
#           2) list of fields for table creation
def getTabProperties(csvFilePath):
  import csv
  csv_filename = csvFilePath
  list_of_rows = []
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
    fieldList =list_of_rows[0]
    valsList = list_of_rows[1]
    fieldList.pop(0)  # revove 2 first: tabTag and date
    fieldList.pop(0)


    tabName= valsList [0]
    return tabName,fieldList
