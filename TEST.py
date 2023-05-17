from datetime import datetime, timedelta
import  pyodbc
import random,string
import os


r='D:\\StationData\\Campbell-CR510\\Raw Data Files'
rawDataFolderslist=os.listdir(r)
for item in rawDataFolderslist:
    if os.path.isdir(os.path.join(r, item)):
        sourcePath= item
        print ("Folder:",item)
    else:
        print("NotFolder", item)

file_names = rawDataFolderslist

for file_name in file_names:
            if
                print("file:", file_name)
            else:
              print("Notfile", file_name)
pbar = tqdm(total=10)
for i in range(10):
    sleep(0.01)
    pbar.update(1)
pbar.close()