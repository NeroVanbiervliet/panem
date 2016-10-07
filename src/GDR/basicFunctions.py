# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:43:52 2016

@author: matthias
"""
#Import our models we made in models.py
from first.models import Bakery,Product,HasProduct,Category,Logging,Account,Order,Product_order,Token,AdyenPayment,PointPayment, CreditTopUp, Ingredient
from django.core.exceptions import ObjectDoesNotExist
import datetime

def add_bakery(nameIn,adressIn,postcodeIn,cityIn,GPSLatIn,GPSLonIn,telephoneIn,websiteIn,openingsIn,descriptionIn,bestelLimitTimeIn,bankAccountIn,taxNumberIn,memberIn,bakerAccountIdIn):
    
    b = Bakery(name = nameIn , adress = adressIn , postcode = postcodeIn, city = cityIn ,GPSLat = GPSLatIn, GPSLon = GPSLonIn, telephone = telephoneIn , website = websiteIn, \
     openings = openingsIn , description = descriptionIn , bestelLimitTime = bestelLimitTimeIn, bankAccount = bankAccountIn, taxNumber = taxNumberIn, member = memberIn,bakerAccountId = bakerAccountIdIn)
    b.save()

    return b
    
def update_bakery(idIn,nameIn,adressIn,postcodeIn,cityIn,GPSLatIn,GPSLonIn,telephoneIn,websiteIn,openingsIn,descriptionIn,bestelLimitTimeIn,bankAccountIn,taxNumberIn,memberIn,bakerAccountIdIn):
    #check if bakery exists    
    try:
        b = Bakery.objects.get(id=idIn)
        b.name = nameIn
        b.adress = adressIn
        b.postcode = postcodeIn
        b.city = cityIn
        b.GPSLat = GPSLatIn
        b.GPSLon = GPSLonIn
        b.telephone = telephoneIn
        b.website = websiteIn
        b.openings = openingsIn
        b.description = descriptionIn
        b.bestelLimitTime = bestelLimitTimeIn
        b.bankAccount = bankAccountIn
        b.taxNumber = taxNumberIn
        b.memberIn = memberIn
        b.bakerAccount = bakerAccountIdIn
        b.save()
        a = 'success'
    except ObjectDoesNotExist:
        a = 'bakerydoesnotexist'
    
    return a

# updates only the provided fields in bakeryInfo
# bakeryInfo.id is required to identify the bakery
def updateBakeryFlexible(bakeryInfo):
    #check if bakery exists
    try:
        b = Bakery.objects.get(id=bakeryInfo['id'])

        # loop over fields available in bakeryInfo
        for key in bakeryInfo.keys():
            if key != 'id':
                setattr(b, key, bakeryInfo[key])

        b.save()
        output = 'success'
    except ObjectDoesNotExist:
        output = 'bakerydoesnotexist'

    return output

def add_product(nameIn,category_idIn,standardIn,fotoIdIn,ingredientsIn):
    
    b = Product(name=nameIn , category_id = category_idIn, standard = standardIn, photoId = fotoIdIn, ingredients=ingredientsIn)
    b.save()
    id = b.id
    
    return id
    
def update_product(idIn,nameIn,category_idIn,standardIn,fotoIdIn,ingredientsIn):
    #check if product exists
    try:
        b = Product.objects.get(id=idIn)
        b.name = nameIn
        b.category_id = category_idIn
        b.standard = standardIn
        b.fotoId = fotoIdIn
        b.ingredients = ingredientsIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol'
        
def add_hasProduct(bakeryIdIn,productIdIn,priceIn,availabilityIn):
    
    b = HasProduct(bakeryId = bakeryIdIn, productId = productIdIn , price = priceIn, availability = availabilityIn)
    b.save()
    
def update_hasProduct(idIn,bakeryIdIn,productIdIn,priceIn,availabilityIn):
    #check if hasproduct exists
    try:
        b = HasProduct.objects.get(id=idIn)
        b.bakeryId = bakeryIdIn
        b.product = productIdIn
        b.price = priceIn
        b.availability = availabilityIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol'
    
def add_category(nameIn):
    
    b = Category(name = nameIn)
    b.save()

def update_category(idIn,nameIn):
    #check if category exists
    try:
        b = Category.objects.get(id=idIn)
        b.name = nameIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol'
        
def add_logging(timeStampIn, accountIn,event_textIn,kindIn):
    
    b = Logging(timeStamp = timeStampIn , account = accountIn , event_text = event_textIn, kind = kindIn)
    b.save()
    
def update_logging(idIn,timeStampIn, accountIn,event_textIn,kindIn):
    #check if logging exists
    try:
        b = Logging.objects.get(id=idIn)
        b.timeStamp = timeStampIn
        b.account = accountIn
        b.event_text = event_textIn
        b.kind = kindIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol'

def add_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, passwordIn, confirmedNumber,salt):
    
    b = Account(firstname = firstnameIn , lastname = lastnameIn , email = emailIn , type = typeIn , adress = adressIn, password = passwordIn, confirmed = confirmedNumber,salt = salt)
    b.save()
    
def update_account(idIn, firstnameIn, lastnameIn, emailIn, typeIn, adressIn, passwordIn):
    #check if account exists    
    try:
        b = Account.objects.get(id=idIn)
        b.firstname = firstnameIn
        b.lastname = lastnameIn
        b.email = emailIn
        b.type = typeIn
        b.adress = adressIn
        b.password = passwordIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol'
        
def add_order(accountIdIn, bakeryIdIn, statusIn, timePickupIn, timeOrderedIn, commentIn,totalPriceIn):
    
    b = Order(accountId = accountIdIn , bakeryId = bakeryIdIn , status = statusIn , timePickup = timePickupIn , timeOrdered = timeOrderedIn , comment = commentIn, totalPrice = totalPriceIn)
    b.save()
    return b.id
    
def update_order(idIn,accountIdIn, bakeryIdIn, statusIn, timePickupIn, timeOrderedIn, commentIn, totalPriceIn):
    #check if order exists
    try:
       b = Order.objects.get(id=idIn)
       b.account = accountIdIn
       b.bakeryId = bakeryIdIn
       b.status = statusIn
       b.timePickup = timePickupIn
       b.timeOrdered = timeOrderedIn
       b.comment = commentIn
       b.totalPrice = totalPriceIn
       b.save()
        
    except ObjectDoesNotExist:
        a = 'lol'       
    
def add_product_order(orderIdIn, productIdIn, amountIn,priceIn):
    
    b = Product_order(orderId = orderIdIn , productId = productIdIn , amount = amountIn,price = priceIn)
    b.save()
    
def update_product_order(idIn, orderIdIn, productIdIn, amountIn, priceIn):
    #check if product order exists
    try:
        b = Product_order.objects.get(id=idIn)
        b.orderId = orderIdIn
        b.productId = productIdIn
        b.amount = amountIn
        b.price = priceIn
        b.save()
    except ObjectDoesNotExist:
        a = 'lol' 

def add_token(valueIn,accountIdIn,expiryIn):
    
    b = Token(value = valueIn, accountId = accountIdIn, expiry = expiryIn)
    b.save()
    
def add_AdyenPayment(date,orderId,shipDate,accountId,bakeryId,clientPay,transactionCosts,extraCredit,succes):
    
    b = AdyenPayment(date=date,orderId=orderId,shipDate=shipDate, accountId=accountId,bakeryId=bakeryId,clientPay=clientPay,transactionCosts=transactionCosts,extraCredit=extraCredit,succes=succes)
    b.save()
    
    return b.id

def addAdyenPaymentForTopUp(account,creditTopUp):

    # NEED transactionCosts, wat mee aanvangen?
    adyenPayment = AdyenPayment(date=creditTopUp.dateOrdered,orderId=creditTopUp.id,shipDate=creditTopUp.dateOrdered,accountId=account.id,bakeryId=0,clientPay=creditTopUp.amountToPay,transactionCosts=0,extraCredit=creditTopUp.amountTopUp,succes=0)
    adyenPayment.save()

    return adyenPayment.id
    
def add_PointPayment(date,orderId,shipDate,accountId,bakeryId,clientPay,succes):
    
    b = PointPayment(date=date,orderId=orderId,shipDate=shipDate, accountId=accountId,bakeryId=bakeryId,clientPay=clientPay,succes=succes)
    b.save()
    
    return b.id

# adds a CreditTopUp item to the database, and returns it
def addCreditTopUp(accountId,amountToPay) :

    # date of today
    today = datetime.datetime.now()
    # promotion : if amountToPay >= 10 euro, then 2 euro is added extra to the top up NEED of enkel de eerste keer?
    amountTopUp = amountToPay + 200*int((amountToPay >= 1000)) # int(True) = 1 and int(False) = 0

    # create new database item
    newDbItem = CreditTopUp(accountId=accountId, dateOrdered=today, amountToPay=amountToPay, amountTopUp=amountTopUp)
    newDbItem.save()

    return newDbItem

# adds an ingredient associated with a bakery
# allergenes are set empty
# returns the id of the created database record
def addBakeryIngredient(bakeryId, name):
    newIngredient = Ingredient(name=name, isStandard=False, bakeryId=bakeryId, allergenes='[]')
    newIngredient.save()
    return newIngredient.id