import time,os,glob
from time import sleep

def removeOld_V2(files,minuteLimit):

    now = time.time()  # time in sec
    s = 0
    for f in files:

            if os.stat(f).st_mtime < now - minuteLimit*60:
                s = s + 1
                if os.path.isfile(f):
                    os.remove(f)
    print("deleted ", s)
    return s
t=0
s = "running" + str(t)
# for i in tqdm(range(20)):
#     s="                 running"+str(t)
#     print(s,end='')
#     t=t+2
#     sleep(0.5)

