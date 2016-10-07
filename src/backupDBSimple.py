# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:20:40 2016

@author: matthias
"""
import datetime
import os
import shutil

fileLocation = "db.sqlite3"
backupLocation = "dbBackup/"
backupTempLocation = "dbBackup/temp/"

backupFreqTemp = 10 #minutes
backupFreqPerm = 2*60 #minutes
backupClearFreqTemp = 3*60 #minutes
backupClearFreqPerm = 24*60*30 #minutes
#backups = os.listdir(backupLocation)
#backupsTemp = os.listdir(backupTempLocation)

running = True
lastTempUpdateTime = datetime.datetime.now()
lastPermUpdateTime = datetime.datetime.now()

while running:
    if (datetime.datetime.now() - lastTempUpdateTime).seconds/60. > backupFreqTemp:
        dst = backupTempLocation + str(datetime.datetime.now())[:19] + '/'
        os.makedirs(dst)
        shutil.copy(fileLocation, dst)
        lastTempUpdateTime = datetime.datetime.now()
    
    
    if (datetime.datetime.now() - lastTempUpdateTime).seconds/60. > backupFreqPerm:
        dst = backupLocation + str(datetime.datetime.now())[:19] + '/'
        os.makedirs(dst)
        shutil.copy(fileLocation, dst)
        lastPermUpdateTime = datetime.datetime.now()
        
    
    backupsTemp = os.listdir(backupTempLocation)
    for date in backupsTemp:
        date_object = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        if (datetime.datetime.now() - date_object).seconds/60. > backupClearFreqTemp:
            shutil.rmtree(backupTempLocation + date)
            
    backups = os.listdir(backupLocation)
    for date in backups:
        if not date == 'temp':
            date_object = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
            if (datetime.datetime.now() - date_object).seconds/60. > backupClearFreqPerm:
                shutil.rmtree(backupLocation + date)
    