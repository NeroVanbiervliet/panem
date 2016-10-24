from GDR.basicFunctions import add_category, add_product, add_hasProduct, add_PointPayment
from first.models import Bakery, Order, Logging, Product, Account, AdyenPayment
from django.core.exceptions import ObjectDoesNotExist
import datetime

def get_all_bakeries():

    try:
        output = Bakery.objects.all()

    except ObjectDoesNotExist:
        output = 'NA'

    return output

## Fillers
## fill category List


#def fill_products():
#    #update for new products
#    f = open('products.csv','r')
#    imageDirectory = '../frontend/images/products/'
#
#    for line in f:
#        [nameIn,fotoUrl,categoryId] = line.split(';')
#        fotoUrl = imageDirectory + fotoUrl
#        try:
#            object = Product.objects.get(name=nameIn)
#            idIn = object.id
#            update_product(idIn,nameIn,fotoUrl,categoryId,1)
#
#        except ObjectDoesNotExist:
#            id = add_product(nameIn,fotoUrl,categoryId,1)
#
#    f.close()

#def fill_bakeries():
#    #update bakery list
#        #update for new products
#    f = open('bakeries.csv','r')
#
#    for line in f:
#        [nameIn,location,telephoneIn,emailIn,websiteIn] = line.replace('\n','').split(';')
#        [adressIn,rest] = location.split(',')
#        postcodeIn = rest[1:5]
#        cityIn = rest[6:]
#
#        if emailIn == 'TODO':
#            emailIn = ''
#        if telephoneIn == 'TODO':
#            telephoneIn = ''
#        if websiteIn == 'TODO':
#            websiteIn = ''
#
#        print adressIn,postcodeIn,cityIn
#
#        GPSLatIn,GPSLonIn = getGpsFromAdress(adressIn + ' ' +  str(postcodeIn))
#
#        print GPSLatIn,GPSLonIn
#
#        try:
#            object = Bakery.objects.get(adress=adressIn)
#            idIn = object.id
#            update_bakery(idIn,nameIn,adressIn,postcodeIn,cityIn,GPSLatIn,GPSLonIn,telephoneIn,emailIn,websiteIn,'','','','','',0)
#            #print 'update'
#        except ObjectDoesNotExist:
#            id = add_bakery(nameIn,adressIn,postcodeIn,cityIn,GPSLatIn,GPSLonIn,telephoneIn,emailIn,websiteIn,'','','','','',0)
#            #print 'new'
#
#    f.close()

def initStandardProducts(bakeryObject):
    products = Product.objects.all()
    bakeryId = bakeryObject.id

    for product in products:
        if product.standard == 1:
            price = 0.0
            availability = 0
            copiedproductId = add_product(product.name,product.category_id,0,product.photoId,product.ingredients)
            add_hasProduct(bakeryId,copiedproductId,price,availability)




# pays the current order with credit if possible
def currentOrderCredit(accountId):
    account = Account.objects.get(id=accountId)
    orderId = account.lastOrderId

    if orderId > 0:
        order = Order.objects.get(id=orderId)
        if account.credit >= order.totalPrice:
            order.status = 'payed;0'
            order.save()
            account.lastOrderId = 0
            account.credit += -order.totalPrice
            account.save()
            pointPaymentId = add_PointPayment(datetime.datetime.now(),orderId,order.timePickup,accountId,order.bakeryId,order.totalPrice,1)
            output = 'success-' + str(pointPaymentId)
        else:
            output = 'notenoughcredits'


    else:
        output = 'nocurrentorder'

    return output


def dataBaseFiller():

    ## Generate Bakeries
    n = 100
    for lol in range(n):
        firstNames = ['Jan','Piet','Joris','Korneel','Louis','Nero','Michiel','Emiel','Maarten','Helena','Suzy','Martine','Lieven']
        lastNames = ['Kok','Jassens','Peters','Baert','Baerto','VDB','Lesc','VBV','Homo','Kaas','Schoenmaker','De Vroe','Mignolet']
        adressList = [['Jozef van Walleghemstraat 11','8200','Brugge'],['Loppemsestraat 80','8020','Oostkamp'],['Raverschootstraat 62','9900','Eeklo'],['Koolstraat 1','8750','Wingene'],['Diepestraat 50','9200','Dendermonde'],['Fonteinstraat 57','9400','Ninove'],['Zevekotestraat 9','9940','Evergem']]


        personInfo = {}
        personInfo['firstName'] = firstNames[random.randint(0,len(firstNames)-1)]
        personInfo['lastName'] = lastNames[random.randint(0,len(lastNames)-1)]
        personInfo['email'] = personInfo['firstName'] + personInfo['lastName'] + '@gmail.com'
        personInfo['password'] = 'password101'

        bakeryInfo = {}
        bakeryInfo['name'] = personInfo['lastName'] + personInfo['firstName'] + str(random.randint(0,100)) + 'bakerij'
        dummy = random.randint(0,len(adressList)-1)
        bakeryInfo['adress'] = adressList[dummy][0]
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
    #create_bakery(personInfo, bakeryInfo, token)

    ## Generate Products for the Bakeries

    ## Generate Accounts
    n = 10

    ## Generate Orders
    n = 400


    return 'lol'