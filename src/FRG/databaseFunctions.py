# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:54:03 2016

@author: matthias
"""

#Import Password protection bcrypt, download on server

#Standard imports, nothing special here
import os
import datetime
import threading

# Asana
import asana

client = asana.Client.basic_auth('0/2efacd6b6fdc030eaac067fc6c151036')

# Set django settings correct, no clue why but internet said so
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panem_project.settings")
import django

django.setup()

#Import our models we made in models.py
from first.models import DisableDates

#Needed to check if obejct exists
from django.core.exceptions import ObjectDoesNotExist

#Import geopy for GPS handling
import geopy
import geopy.distance

#Import basic functions (add,update)
from GDR.basicFunctions import *
import FRG.wareHouse as wrh


## Get objects

def get_bakeryId(name_lookup):
    try:
        objectOut = Bakery.objects.get(name=name_lookup)
    except ObjectDoesNotExist:
        objectOut = 'NA'
        
    return objectOut

def get_bakery_from_id(bakeryId,accountId):
    try:
        objectOut = Bakery.objects.get(id=bakeryId)
        bakeryIdStr = str(bakeryId)
        logVisit(accountId,bakeryIdStr)
    except ObjectDoesNotExist:
        objectOut = 'NA'
        
    return objectOut


def get_allProducts():

    output = []
    products = Product.objects.all()
    for product in products:
        temp = {}
        temp['name'] = product.name
        temp['id'] = product.id
        temp['category'] = product.category_id
        temp['standard'] = product.standard
        temp['available'] = product.available
        temp['ingredients'] = product.ingredients
        
        output.append(temp)
        
    return output


def adapt_bakery(bakeryInfo):
    adress = bakeryInfo['adress'] + ' ' + str(bakeryInfo['postcode']) +' '+ bakeryInfo['city']
    GPSLat,GPSLon = getGpsFromAdress(adress)
    output = update_bakery(bakeryInfo['id'],bakeryInfo['name'],bakeryInfo['adress'],int(bakeryInfo['postcode']),bakeryInfo['city'],GPSLat,GPSLon,bakeryInfo['telephone'],bakeryInfo['website'],bakeryInfo['openings'],bakeryInfo['description'],bakeryInfo['bestelLimitTime'],bakeryInfo['bankAccount'],bakeryInfo['taxNumber'],bakeryInfo['member'],bakeryInfo['bakerAccountId'])
    return output


def get_offer_bakery(bakeryId):
    #list the offer (aka all his products)
    try:
        Bakery.objects.get(id=bakeryId)
        categories = Category.objects.all()
        
        resultArray1 = []
        resultDict2 = {}    
        
        for i in range(len(categories)):
            tempDict = {'name' : str(categories[i].name), 'products' : []}
            
            a = HasProduct.objects.all()
            for object1 in a:
                if object1.bakeryId == bakeryId:
                    dummy_id = object1.productId
                    product = Product.objects.get(id = dummy_id)

                    if product.category_id == categories[i].id:
                        tempDict['products'].append(str(product.id))
                        resultDict2[str(product.id)] = {'name' : str(product.name), 'price' : float(object1.price)}
                      
                        
            resultArray1.append(tempDict)
            
    except ObjectDoesNotExist:
        resultArray1,resultDict2 = 'NA','NA'
    
    return resultArray1,resultDict2

def get_products_bakery(bakeryId):

    try:
        Bakery.objects.get(id=bakeryId)
        hasproducts = HasProduct.objects.all()
        allIngredients = Ingredient.objects.all()
        output = []
 
        for hasproduct in hasproducts:
            if hasproduct.bakeryId == bakeryId:
                product = Product.objects.get(id=hasproduct.productId)
                tempDict = {}
                tempDict['id'] = hasproduct.productId
                tempDict['name'] = product.name
                tempDict['categoryid'] = product.category_id
                tempDict['price'] = hasproduct.price
                tempDict['available'] = hasproduct.availability
                tempDict['photoId'] = product.photoId

                # ingredients
                tempDict['ingredients'] = []
                ingredientIds = eval(product.ingredients)
                for i in range(len(ingredientIds)):
                    try:
                        curIng = Ingredient.objects.get(id=int(ingredientIds[i]))
                        curType = 'standard' if curIng.isStandard else 'custom'
                        tempDict['ingredients'].append({'id':curIng.id, 'name':curIng.name, 'type':curType})
                    except ObjectDoesNotExist:
                        raise NameError('ingredient not found with id ' + str(int(ingredientIds[i])))

                allergenes = wrh.ingredients2Allergenes(allIngredients,product.ingredients)
                tempDict['allergenes'] = allergenes
                output.append(tempDict)
            
    except ObjectDoesNotExist as e:
        # exception can be cause by one of the TWO get operations above (retrieving a bakery object or a product object)
        output = "Exception: " + str(e)
    
    return output


def get_products_category_bakery(bakeryId):
    
    products = get_products_bakery(bakeryId)
    categories = Category.objects.all()
    output = []
    productsPerCategory = {}
    names = {}
    photoIds = {}
    for category in categories:
        productsPerCategory[str(category.id)] = [] # initialise empty product list for a category
        names[str(category.id)] = category.name
        photoIds[str(category.id)] = category.defaultPhotoId

    if type(products) == type('a string variable'): # products is an error message instead of an array
        return str(products)
    else:
        for product in products:
            categoryId = product['categoryid']
            productsPerCategory[str(categoryId)].append(product)

        # refactor data for output
        for key in productsPerCategory:
            if len(productsPerCategory[key]) > 0:
                temp2Dict = {}
                temp2Dict['name'] = names[key]
                temp2Dict['products'] = productsPerCategory[key]
                temp2Dict['id'] = key
                temp2Dict['defaultPhotoId'] = photoIds[key]
                output.append(temp2Dict)
        
        return output

def get_disableDates(bakeryId):
    
    output = []
    threshold = 40    
    
    try: 
        bakery = Bakery.objects.get(id = bakeryId)
        
        allDisableDates = DisableDates.objects.all()
        for disableDate in allDisableDates:
            
            diff = (disableDate.date.date() - datetime.datetime.now().date()).days
            if disableDate.bakeryId == bakeryId and -1 < diff < threshold:
                output.append(diff)
        
        openings = eval(bakery.openings)
        weekdayNow = datetime.datetime.now().weekday()
        
        for i in range(len(openings)):
            weekday = i
            if openings[i][2] == 'false':
                for i in range(7):
                    daysInFuture = weekday - weekdayNow + 7*i
                    if -1 < daysInFuture < threshold and (daysInFuture not in output):
                        output.append(daysInFuture)
        output.sort()
    except ObjectDoesNotExist:
        output = 'Bakery does not exist'
    
    return output


# NEED wordt nergens gebruikt
def getpassword():
    #TODO: password uitlezen vanuit een file
    return 'suzie2000'
    
    
def getGpsFromAdress(adress):
    #TODO: voeg een check to als het gelukt is, zoniet default waardes doorgeven
    geolocator = geopy.Nominatim()
    try:
        location = geolocator.geocode(adress)
        GPSLat,GPSLon = location.latitude,location.longitude
    except:
        GPSLat,GPSLon = 0,0
    
    return GPSLat,GPSLon


def asanaLink(assigneeEmail,taskName,notes):
    a={'name':taskName,'projects':'151047700474054','workspace':'97640907304377','notes':notes,'assignee':assigneeEmail}
    client.tasks.create(a)

def logVisit(accountId,bakeryId):
    newLog = Logging()
    newLog.timeStamp = datetime.datetime.now()
    newLog.accountId = accountId
    newLog.event_text = bakeryId
    newLog.kind = 'visit'

    newLog.save()


def LogHappenning(accountId,event_text,kind):
    b = Logging()
    
    b.timeStamp = datetime.datetime.now()
    b.accountId = accountId
    b.event_text = event_text
    b.kind = kind
    
    b.save()

    if kind == 'test':
        taskName = 'issue ' + str(b.id) + ' [' + kind + ']'
        notes = 'Dit is een test over issue ' + str(b.id) + '.\n' \
                + event_text
    
    elif kind == 'contact':
        taskName = 'issue ' + str(b.id) + ' [' + kind + ']'
        notes = 'account id : ' + str(b.accountId) + '\n' +\
                b.event_text

    else:
        taskName = 'issue ' + str(b.id)
        notes = 'account id : ' + str(b.accountId) + '\n' +\
                'event text : ' + b.event_text


    # save task to asana
    asanaThread = threading.Thread(target=asanaLink, args=['baert_nr1@msn.com',taskName,notes])
    asanaThread.start()
    #asanaLink('baert_nr1@msn.com',taskName,notes)



