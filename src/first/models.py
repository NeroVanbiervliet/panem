from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Bakery(models.Model):
    name = models.CharField(max_length=50, default='')
    adress = models.CharField(max_length=200, default='')
    postcode = models.IntegerField(default=0)
    city = models.CharField(max_length=200, default='')
    GPSLat = models.DecimalField(max_digits=15, decimal_places=10,default = 0)
    GPSLon = models.DecimalField(max_digits=15, decimal_places=10,default = 0)
    telephone = models.CharField(max_length=12, default='')
    website = models.CharField(max_length=100, default='')
    openings = models.CharField(max_length=600, default='')
    description = models.CharField(max_length=300, default='')
    bestelLimitTime = models.CharField(max_length=10, default='')
    bankAccount = models.CharField(max_length=10, default='')
    taxNumber = models.CharField(max_length=20, default='')
    member = models.IntegerField(default=0) #0=no member, 1= member TODO beter een boolean isMember?
    bakerAccountId = models.IntegerField(default=0)
    photoId = models.IntegerField(default=0)
    emailNotifyNextDayOrder = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=50, default='')
    category_id = models.IntegerField(default=0)
    standard = models.IntegerField(default=0)
    photoId = models.IntegerField(default=0)
    ingredients = models.CharField(max_length=500, default='[]')
    
    def __str__(self):
        return self.name
        
class HasProduct(models.Model):
    bakeryId = models.IntegerField(default=0)
    productId = models.IntegerField(default=0)
    price = models.IntegerField(default=0) #in cent euro
    availability = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.bakeryId) + '-' + str(self.productId)
        
class Category(models.Model):
    name = models.CharField(max_length=50, default='')
    defaultPhotoId = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
        
class Logging(models.Model):
    timeStamp = models.DateTimeField(default=0)
    accountId = models.IntegerField(default=0)
    event_text = models.CharField(max_length=500, default='')
    kind = models.CharField(max_length=20, default='')
    
    def __str__(self):
        return str(self.timeStamp)

class Account(models.Model):
    firstname = models.CharField(max_length=20, default='')
    lastname = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=254, default='')
    type = models.CharField(max_length=10, default='') #normal/baker/super
    adress = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    confirmed = models.IntegerField(default=0)
    salt = models.CharField(max_length=200, default='')
    language = models.CharField(max_length=200, default='nl')
    shopperReference = models.CharField(max_length=100, default='')
    credit = models.IntegerField(default=0)
    lastOrderId = models.IntegerField(default=0)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname

class Order(models.Model):
    accountId =  models.IntegerField(default=0)
    bakeryId = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='')
    timePickup =  models.DateTimeField()
    timeOrdered = models.DateTimeField()
    comment = models.CharField(max_length=100, default='')
    totalPrice = models.IntegerField(default=0)
    
        
    def __str__(self):
        return str(self.id)

class CreditTopUp(models.Model):
    accountId =  models.IntegerField(default=0)
    dateOrdered = models.DateTimeField()
    amountToPay = models.IntegerField(default=0) # total to pay
    amountTopUp = models.IntegerField(default=0) # increase in credit on account, dan differ from amountToPay due to a promotion
    status = models.CharField(max_length=100, default='created')

    def __str__(self):
        return str(self.id)

class Product_order(models.Model):
    orderId = models.IntegerField(default=0)
    productId = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.orderId)
        
class Token(models.Model):
    value = models.CharField(max_length=200, default='')
    accountId = models.IntegerField(default=0)
    expiry = models.DateTimeField()
    
    def __str__(self):
        return str(self.value)
        
class AdyenPayment(models.Model):
    date = models.DateTimeField()
    orderId = models.IntegerField(default=0)
    shipDate = models.DateTimeField()
    accountId = models.IntegerField(default=0)
    bakeryId = models.IntegerField(default=0)
    clientPay = models.DecimalField(max_digits=15, decimal_places=3,default = 0)
    transactionCosts = models.DecimalField(max_digits=15, decimal_places=3,default = 0)
    extraCredit = models.DecimalField(max_digits=15, decimal_places=3,default = 0)
    succes = models.IntegerField(default=0)
    isCreditTopUp = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.date)[:19] +' '+ str(self.accountId)
        
class PointPayment(models.Model):
    date = models.DateTimeField()
    orderId = models.IntegerField(default=0)
    shipDate = models.DateTimeField()
    accountId = models.IntegerField(default=0)
    bakeryId = models.IntegerField(default=0)
    clientPay = models.DecimalField(max_digits=15, decimal_places=3,default = 0)
    succes = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.date) +' '+ str(self.accountId)
        
class Ingredient(models.Model):
    name = models.CharField(max_length=200, default='')
    allergenes = models.CharField(max_length=200, default='[]')
    isStandard = models.BooleanField(default=True)
    bakeryId = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class DisableDates(models.Model):
    bakeryId = models.IntegerField(default=0)
    date = models.DateTimeField()
    
    def __str__(self):
        return str(self.bakeryId)

class PromoCode(models.Model):
    type = models.CharField(max_length=10, default='')
    valueOne = models.IntegerField()
    isUsed = models.BooleanField(default=False)