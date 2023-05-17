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
    fieldString =list_of_rows[0]
    valsString = list_of_rows[1]
    fieldString.pop(0)  # revove 2 first: tabTag and date
    fieldString.pop(0)

    tabName= valsString [0]
    return tabName,fieldString
