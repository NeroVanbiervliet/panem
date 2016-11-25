# -*- coding: utf-8 -*-
"""
Created on 22:38:43 2016

@author: matthias
"""
import random
import datetime

from FRG.databaseFunctions import get_allProducts, get_products_category_bakery,updateFunction
from FRG.wareHouse import adaptProducts
from FRG.creatorFunctions import create_bakery,create_account
from GDR.basicFunctions import add_product,add_category,addBakeryIngredient,updateFunction
from first.models import Bakery,Category,Order,Product_order,Account,HasProduct
import FRG.salesOffice as slo
import GDR.basicFunctions as bsf

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
    fillPromoCodesCredit()
    print 'Succes Promo Codes'
    fillSomeOrders()
    print 'Succes Orders'



def databaseFillCategory():
    #only developers mode
    add_category('Broden',1)
    add_category('Koffiekoeken',2)
    add_category('Klein gebak',3)
    add_category('Taarten',4)
    add_category('Broodjes en Pistolets',5)

def databaseFillStandardProducts():
    ## Add products
    standardProducts = [['Wit brood','Broden',10], \
                        ['Bruin brood', 'Broden',11], \
                        ['Volkoren brood', 'Broden',12], \
                        ['Tijger brood', 'Broden',13], \
                        ['Eerlijk brood', 'Broden',14], \
                        ['Zwart brood', 'Broden',15], \
                        ['Croissant','Koffiekoeken',16], \
                        ['Chocoladekoek','Koffiekoeken',17], \
                        ['Lange Suisse','Koffiekoeken',18], \
                        ['Ronde Suisse','Koffiekoeken',19], \
                        ['Tompouce','Klein gebak',20], \
                        ['Profiterollekes','Klein gebak',21], \
                        ['Muffin','Klein gebak',22], \
                        ['Witte Taart','Taarten',23], \
                        ['Voetbal Taart','Taarten',24], \
                        ['Smurfen Taart','Taarten',25], \
                        ['Aardbei Taart','Taarten',26], \
                        ['Framboos Taart','Taarten',27], \
                        ['Framblij Taart','Taarten',28], \
                        ['Sandwich','Broodjes en Pistolets',29], \
                        ['Picollo','Broodjes en Pistolets',30], \
                        ['Pistolet','Broodjes en Pistolets',31]]

    for item in standardProducts:
        category = Category.objects.get(name=item[1])
        add_product(item[0],category.id,1,item[2],[])

    ## Add Ingredients
    ingredientsList = ['meel','tarwe','ei','bloem','rozijnen','chocolade','water','suiker','zout','peper','panda','geitenkaas','melk']
    allergenesList = ['Gluten','Schaaldieren','Eieren','Vis','Pinda','Soja','Melk','Noten','Slederij','Mosterd','Sesamzaad','Zwaveldioxide','Lupine','Weekdieren','Weekenddieren']

    for name in ingredientsList:
        amount = random.randint(1,3)
        allergenes = []
        for i in range(amount):
            allergene = allergenesList[random.randint(0,len(allergenesList)-1)]
            if not allergene in allergenes:
                allergenes.append(allergene)
        addBakeryIngredient(0,name,True,allergenes)




def databaseFillBakeries():

    ## Generate Bakeries
    bakerN = 200
    for lol in range(bakerN):

        if lol%5 == 0:
            print "bakery progress = " + str(lol) + "/" + str(bakerN)

        firstNames = ['Jan','Piet','Joris','Korneel','Louis','Nero','Michiel','Emiel','Maarten','Helena','Suzy','Martine','Lieven']
        lastNames = ['Kok','Jassens','Peters','Baert','Baerto','VDB','Lesc','VBV','Homo','Kaas','Schoenmaker','De Vroe','Mignolet']
        adressList = [['Jozef van Walleghemstraat 11','8200','Brugge'],['Loppemsestraat 80','8020','Oostkamp'],['Raverschootstraat 62','9900','Eeklo'],['Koolstraat 1','8750','Wingene'],['Diepestraat 50','9200','Dendermonde'],['Fonteinstraat 57','9400','Ninove'],['Zevekotestraat 9','9940','Evergem']]
        bakeryPrefix = ['Krokante','Warme','Verse','Dagelijkse','','Lokale','Lekkere','Gebakken','Bakkers']
        bakerySuffix = [['Het','Croissantje'],['Het','Brood'],['De','Bakker'],['Het','Huis'],['','Stefaan'],['','Margriet'],['De','Patissier'],['Het','Hok'],['Het','Paleis']]

        personInfo = {}
        personInfo['firstName'] = firstNames[random.randint(0,len(firstNames)-1)]
        personInfo['lastName'] = lastNames[random.randint(0,len(lastNames)-1)]
        personInfo['email'] = personInfo['firstName'] + personInfo['lastName'] + str(random.randint(0,100))+ '@gmail.com'
        personInfo['password'] = 'rosbeiaard'

        bakeryInfo = {}
        suff = bakerySuffix[random.randint(0,len(bakerySuffix)-1)]
        bakeryInfo['name'] = suff[0] + ' ' + bakeryPrefix[random.randint(0,len(bakeryPrefix)-1)] + ' ' + suff[1]
        dummy = random.randint(0,len(adressList)-1)

        bakeryInfo['street'] = adressList[dummy][0]
        bakeryInfo['postcode'] = adressList[dummy][1]
        bakeryInfo['city'] = adressList[dummy][2]
        bakeryInfo['telephone'] = random.randint(10**5,10**6)

        openings = [[{"h":"4","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False],[{"h":"6","m":"30"},{"h":"19","m":""},False]]
        for i in range(len(openings)):
            openings[i][2] = bool(random.getrandbits(1)) # random boolean
            openings[i][0]['h'] = str(random.randint(5,7))
            openings[i][0]['m'] = str(random.randint(0,40))
            openings[i][1]['h'] = str(random.randint(16,20))
            openings[i][1]['m'] = str(random.randint(0,40))

        openings = str(openings)
        openings = openings.replace('\'','\"').replace('False','false').replace('True','true')

        bakeryInfo['openings'] = openings
        bakeryInfo['bankAccount'] = str(random.randint(10**5,10**6))
        bakeryInfo['taxNumber'] = str(random.randint(10**5,10**6))
        bakeryInfo['website'] = "nero.be"

        token = 'haha'

        # sendMail = False
        output = create_bakery(personInfo, bakeryInfo, False)
        if not output == 'success':
            print output

        else:
            # change photoID
            object = Bakery.objects.get(taxNumber=bakeryInfo['taxNumber'])
            updates = {}
            updates['photoId'] = random.randint(1,7)
            output = updateFunction(object, updates)

    # default baker
    personInfo = {}
    personInfo['firstName'] = "Sloe"
    personInfo['lastName'] = "Wie"
    personInfo['email'] = "sloewie@gmail.com"
    personInfo['password'] = 'rosbeiaard'

    bakeryInfo = {}
    bakeryInfo['name'] = "Bakkermans Nero"
    bakeryInfo['street'] = "damse vaart zuid 14"
    bakeryInfo['postcode'] = 8310
    bakeryInfo['city'] = "Brugge"
    bakeryInfo['telephone'] = random.randint(10**5,10**6)
    openings = "[[{\"h\": \"5\", \"m\": \"15\"}, {\"h\": \"16\", \"m\": \"28\"}, true], [{\"h\": \"7\", \"m\": \"28\"}, {\"h\": \"18\", \"m\": \"16\"}, false], [{\"h\": \"7\", \"m\": \"32\"}, {\"h\": \"18\", \"m\": \"4\"}, false], [{\"h\": \"5\", \"m\": \"13\"}, {\"h\": \"16\", \"m\": \"40\"}, true], [{\"h\": \"5\", \"m\": \"26\"}, {\"h\": \"17\", \"m\": \"1\"}, true], [{\"h\": \"5\", \"m\": \"35\"}, {\"h\": \"18\", \"m\": \"8\"}, true], [{\"h\": \"5\", \"m\": \"28\"}, {\"h\": \"20\", \"m\": \"6\"}, true]]"
    bakeryInfo['openings'] = str(openings)
    bakeryInfo['bankAccount'] = str(random.randint(10**5,10**6))
    bakeryInfo['taxNumber'] = str(random.randint(10**5,10**6))
    bakeryInfo['website'] = "nero.be"

    token = 'haha'

    # sendMail = False
    output = create_bakery(personInfo, bakeryInfo, False)
    if not output == 'success':
            print output

    else:
        # change photoID
        object = Bakery.objects.get(taxNumber=bakeryInfo['taxNumber'])
        updates = {}
        updates['photoId'] = random.randint(1,7)
        output = updateFunction(object, updates)

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
#                product['price'] = random.randint(50,1000)
                if category['name'] == 'Taarten':
                    product['price'] = 5*int(random.randint(800,3000)/5)
                elif category['name'] == 'Broden':
                    product['price'] = 5*int(random.randint(150,300)/5)
                elif category['name'] == 'Klein gebak' or category['name'] == 'Koffiekoeken':
                    product['price'] = 5*int(random.randint(80,200)/5)
                else:
                    product['price'] = 5*int(random.randint(80,100)/5)

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
        password = 'rosbeiaard'

        output = create_account(firstname, lastname, email, type, adress, password, False)
        if not output == 'success':
            print output
        #give everyone millions of credit?

    # default accounts
    create_account("Nero","Vanbiervliet","nero.vanbiervliet@gmail.com","normal","damse vaart","rosbeiaard",False)

def fillPromoCodesCredit():

    bsf.addPromoCodeCredit('TESTCODE1')
    slo.usePromoCode('TESTCODE1')
    for i in range(2,100):
        bsf.addPromoCodeCredit('TESTCODE'+str(i))

def fillSomeOrders():
    bakerynero = Bakery.objects.get(name='Bakkermans Nero')
    accounts = Account.objects.filter(type='normal')
    account = accounts[random.randint(0,len(accounts)-1)]

    hasproducts = HasProduct.objects.filter(bakeryId=bakerynero.id, availability=True)

    for i in range(2):
        order = Order()
        order.save()
        updates = {}
        updates['accountId'] = account.id
        updates['bakeryId'] = bakerynero.id
        updates['status'] = 'progress'
        updates['timePickup'] = datetime.datetime.now() + datetime.timedelta(days=2)
        updates['timeOrdered'] = datetime.datetime.now()
        updateFunction(order, updates)

        totalPrice = 0.0
        for i in range(4):
            hasproduct = hasproducts[random.randint(0,len(hasproducts)-1)]
            amount = random.randint(1,5)
            totalPrice += hasproduct.price*amount
            model = Product_order()
            model.save()
            updates2 = {}

            updates2['orderId'] = order.id
            updates2['productId'] = hasproduct.productId
            updates2['amount'] = amount
            updates2['price'] = hasproduct.price
            updateFunction(model, updates2)


        updates['totalPrice'] = totalPrice
        updateFunction(order, updates)
