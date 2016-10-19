# -*- coding: utf-8 -*-
"""
Created on 22:38:43 2016

@author: matthias
"""
import random

from FRG.databaseFunctions import get_allProducts, get_products_category_bakery
from FRG.wareHouse import adaptProducts
from FRG.creatorFunctions import create_bakery,create_account
from GDR.basicFunctions import add_product,add_category
from first.models import Bakery,Category

def databaseFillAll():
    print 'Start'
    databaseFillCategory()
    print 'Succes Category'
    databaseFillStandardProducts()
    print 'Succes Standard Products'
    databaseFillBakeries()
    print 'Succes Bakeries'
    databaseFillProducts()
    print 'Succes Products'
    databaseFillAccounts()
    print 'Succes Accounts'

    

def databaseFillCategory():
    #only developers mode
    add_category('Broden')
    add_category('Koffiekoeken')
    add_category('Klein gebak')
    add_category('Taarten')
    add_category('Broodjes en Pistolets')
    
def databaseFillStandardProducts():
    standardProducts = [['Wit brood','Broden'], \
                        ['Bruin brood', 'Broden'], \
                        ['Volkoren brood', 'Broden'], \
                        ['Tijger brood', 'Broden'], \
                        ['Eerlijk brood', 'Broden'], \
                        ['Zwart brood', 'Broden'], \
                        ['Croissant','Koffiekoeken'], \
                        ['Chocoladekoek','Koffiekoeken'], \
                        ['Lange Suisse','Koffiekoeken'], \
                        ['Ronde Suisse','Koffiekoeken'], \
                        ['Tompouce','Klein gebak'], \
                        ['Profiterollekes','Klein gebak'], \
                        ['Muffin','Klein gebak'], \
                        ['Witte Taart','Taarten'], \
                        ['Voetbal Taart','Taarten'], \
                        ['Smurfen Taart','Taarten'], \
                        ['Aardbei Taart','Taarten'], \
                        ['Framboos Taart','Taarten'], \
                        ['Framblij Taart','Taarten'], \
                        ['Sandwich','Broodjes en Pistolets'], \
                        ['Picollo','Broodjes en Pistolets'], \
                        ['Pistolet','Broodjes en Pistolets']]
                        
    for item in standardProducts:
        category = Category.objects.get(name=item[1])
        add_product(item[0],category.id,1,0,[])


def databaseFillBakeries():

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
        
        adress = adressList[random.randint(0,len(adressList)-1)]
        adress= adress[0] + ' ' + adress[1] + ' ' + adress[2]        
        bakeryInfo['address'] = adress
#        bakeryInfo['address'] = adressList[dummy][0]
#        bakeryInfo['postcode'] = adressList[dummy][1]
#        bakeryInfo['city'] = adressList[dummy][2]
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
        if not output == 'success':
            print output

def databaseFillProducts():
    ## Generate Products for the Bakeries
    bakeries = Bakery.objects.all()
    ingredientsList = ['meel','tarwe','ei','bloem','rozijnen','chocolade','water','suiker','zout','peper','panda','geitenkaas','melk']
    
    for bakery in bakeries:
        
        productUpdate = get_products_category_bakery(bakery.id)
        booleans = [True,False]
        for category in productUpdate:
            for product in category['products']:
                random.randint(0,1)
                product['available'] = booleans[random.randint(0,1)]
                product['price'] = random.randint(50,1000)
                product['ingredients'] = []
                amountOfIngredients = random.randint(1,5)
                for i in range(amountOfIngredients):
                    temp = {}
                    temp['name'] = ingredientsList[random.randint(0,len(ingredientsList)-1)]
                    product['ingredients'].append(temp)
                 
        
        deleteList = []
        output = adaptProducts(bakery.id, productUpdate, deleteList)
        if not output == 'success':
            print output
        

def databaseFillAccounts():
    ## Generate Accounts
    accountN = 10
    firstNames = ['Jan','Piet','Joris','Korneel','Louis','Nero','Michiel','Emiel','Maarten','Helena','Suzy','Martine','Lieven']
    lastNames = ['Kok','Jassens','Peters','Baert','Baerto','VDB','Lesc','VBV','Homo','Kaas','Schoenmaker','De Vroe','Mignolet']
    adressList = [['Jozef van Walleghemstraat 11','8200','Brugge'],['Loppemsestraat 80','8020','Oostkamp'],['Raverschootstraat 62','9900','Eeklo'],['Koolstraat 1','8750','Wingene'],['Diepestraat 50','9200','Dendermonde'],['Fonteinstraat 57','9400','Ninove'],['Zevekotestraat 9','9940','Evergem']]

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
        if not output == 'success':
            print output
        #give everyone millions of credit?


