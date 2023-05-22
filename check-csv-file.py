import csv,easygui
# it not works on confreader/ why?
def check_empty_fields1(csv_filename): # with gui
    isok=True


    with open(csv_filename) as csv_file:
        row_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if not row:
                isok = False
                easygui.msgbox("CSV File has empty row")
        csv_file.seek(0)


        for row in csv_reader:
            col_count = 0
            for col in row:
                if col == "":
                    isok=False
                    print("Found empty field at row: {}, col: {}".format(row_count, col_count))
                    easygui.msgbox("Found empty field at row: {}, col: {}".format(row_count, col_count))
                col_count += 1
            row_count += 1
    return isok

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
#isok=  check_empty_fields1('t.csv')
print (isok)