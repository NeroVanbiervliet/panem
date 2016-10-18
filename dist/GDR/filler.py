# -*- coding: utf-8 -*-
"""
Created on 22:38:43 2016

@author: matthias
"""
import random

from FRG.databaseFunctions import get_allProducts
from FRG.wareHouse import adaptProducts
from FRG.creatorFunctions import create_bakery,create_account

def dataBaseFillBakeries():

    ## Generate Bakeries
    bakerN = 100
    for lol in range(bakerN):
        firstNames = ['Jan','Piet','Joris','Korneel','Louis','Nero','Michiel','Emiel','Maarten','Helena','Suzy','Martine','Lieven']
        lastNames = ['Kok','Jassens','Peters','Baert','Baerto','VDB','Lesc','VBV','Homo','Kaas','Schoenmaker','De Vroe','Mignolet']
        adressList = [['Jozef van Walleghemstraat 11','8200','Brugge'],['Loppemsestraat 80','8020','Oostkamp'],['Raverschootstraat 62','9900','Eeklo'],['Koolstraat 1','8750','Wingene'],['Diepestraat 50','9200','Dendermonde'],['Fonteinstraat 57','9400','Ninove'],['Zevekotestraat 9','9940','Evergem']]


        personInfo = {}
        personInfo['firstName'] = firstNames[random.randint(0,len(firstNames)-1)]
        personInfo['lastName'] = lastNames[random.randint(0,len(lastNames)-1)]
        personInfo['email'] = personInfo['firstName'] + personInfo['lastName'] + str(random.randint(0,100))+ '@gmail.com'
        personInfo['password'] = 'password101'

        bakeryInfo = {}
        bakeryInfo['name'] = personInfo['lastName'] + ' ' + personInfo['firstName'] + ' ' + str(random.randint(0,100)) + ' ' + 'bakerij'
        dummy = random.randint(0,len(adressList)-1)
        
        bakeryInfo['address'] = adressList[dummy][0]
        bakeryInfo['postcode'] = adressList[dummy][1]
        bakeryInfo['city'] = adressList[dummy][2]
        bakeryInfo['telephone'] = random.randint(10**5,10**6)
        openings = [[{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0]]
        for i in range(len(openings)):
            openings[i][2] = random.randint(0,1)
            openings[i][0]['h'] = random.randint(5,7)
            openings[i][0]['m'] = random.randint(0,40)
            openings[i][1]['h'] = random.randint(16,20)
            openings[i][1]['m'] = random.randint(0,40)

        bakeryInfo['openings'] = str(openings)
        bakeryInfo['bankAccount'] = str(random.randint(10**5,10**6))
        bakeryInfo['taxNumber'] = str(random.randint(10**5,10**6))

        token = 'haha'
        
        output = create_bakery(personInfo, bakeryInfo, token)
        print output

#def dataBaseFillProducts():
#    ## Generate Products for the Bakeries
#    # get all products from bakery(standard ones)
#    # alter availablity and price
#    # adaptProducts(bakeryId, productUpdate, deleteList)
#    
#    ## Add some new products to the database
#    # add product
#    # randomly add it to bakeries
#
#def dataBaseFillIngredients():
#    ## Add ingredients to products
#    # get all products and add some ingredients to it
#    
#
def dataBaseFillAccounts():
    ## Generate Accounts
    accountN = 10
    firstNames = ['Jan','Piet','Joris','Korneel','Louis','Nero','Michiel','Emiel','Maarten','Helena','Suzy','Martine','Lieven']
    lastNames = ['Kok','Jassens','Peters','Baert','Baerto','VDB','Lesc','VBV','Homo','Kaas','Schoenmaker','De Vroe','Mignolet']
    adressList = [['Jozef van Walleghemstraat 11','8200','Brugge'],['Loppemsestraat 80','8020','Oostkamp'],['Raverschootstraat 62','9900','Eeklo'],['Koolstraat 1','8750','Wingene'],['Diepestraat 50','9200','Dendermonde'],['Fonteinstraat 57','9400','Ninove'],['Zevekotestraat 9','9940','Evergem']]
    
    personInfo = {}

    for lol in range(accountN):
        firstname= firstNames[random.randint(0,len(firstNames)-1)]
        lastname = lastNames[random.randint(0,len(lastNames)-1)]
        adress = adressList[random.randint(0,len(adressList)-1)]
        adress= adress[0] + ' ' + adress[1] + ' ' + adress[2]
        email = firstname + lastname + '_456' + '@gmail.com'
        type = 'normal'
        password = 'password101'
        token = 'haha'
        
        output = create_account(firstname, lastname, email, type, adress, password,token)
        print output
        #give everyone millions of credit?

#def dataBaseFillOrders():  
#    ## Generate Orders
#    orderN = 400
#    for lol in range(orderN):
#        a = 123
#        # choose bakery
#        # choose account
#        # choose date in the past
#        # choose products to order and amount
#        # pay with credit?
#        
#
#    return 'lol'
