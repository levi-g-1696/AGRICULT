from datetime import datetime, timedelta
import  pyodbc
import random,string
import os
import tqdmtest, time
from tqdm import tqdm



pbar = tqdm(total=10)
for i in range(10):
    time.sleep(0.1)
    pbar.update(1)
pbar.close()