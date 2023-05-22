import logging
import os
from datetime import datetime
from getTabProps import  getTabProperties

import globalConfig

sourceFileErrorLog=os.path.join(globalConfig.logDirectory, "sourceFileError")
def logDataFillError (csvFile,codeErr):
    logging.basicConfig(filename=sourceFileErrorLog, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')
    name,x= getTabProperties(csvFile)
    logging.info("," +name + "," + codeErr)
    return
