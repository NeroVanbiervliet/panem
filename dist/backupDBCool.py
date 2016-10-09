# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 18:19:50 2016

@author: matthias
"""

import datetime
import os
import shutil
import time
import numpy as np

fileLocation = "db.sqlite3"
backupLocation = "dbBackup/"

backupFreq = 5 #minutes

clearM = 0.3
clearQ = -60 #minutes

running = True
lastUpdateTime = datetime.datetime.now()


while running:
    
    if (datetime.datetime.now() - lastUpdateTime).seconds/60. > backupFreq:
        dst = backupLocation + str(datetime.datetime.now())[:19] + '/'
        os.makedirs(dst)
        shutil.copy(fileLocation, dst)
        lastUpdateTime = datetime.datetime.now()
        time.sleep(1)
        
    backups = os.listdir(backupLocation)
    backups = sort(backups)
    i = 0
    while i < len(backups)-2:
        date1 = backups[i]
        date2 = backups[i+1]
        
        date_object1 = datetime.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date_object2 = datetime.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")
        
        minutesDiff = (date_object2 - date_object1).seconds/60.
        minutesAgo = (datetime.datetime.now() - date_object1).seconds/60.        
        
        if minutesDiff < clearM*minutesAgo + clearQ:
            backups = np.delete(backups,i+1)
            shutil.rmtree(backupLocation + date2)
        else:
            i += 1
            