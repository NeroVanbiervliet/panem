# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 17:26:08 2016

@author: matthias
"""
from FRG import databaseFunctions

#databaseFunctions.fill_category()
#datdatabaseFunctionsabaseFunctions.fill_bakery_from_file()
#databaseFunctions.new_bakery_full()

array1,dict1 = databaseFunctions.offer_of_bakery(631)
print array1
print 
print dict1

#product_array = [[22,5],[23,10]]
#account_id = 2
#bakery_id = 631
#time_pickup = datetime.datetime(2020,01,01)
#comment = 'test order'
#
#out = databaseFunctions.make_new_order(product_array, account_id, bakery_id, time_pickup, comment)
#
#print out