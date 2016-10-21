from GDR import basicFunctions as bsf
import GDR.basicFunctions as bsf
from GDR.basicFunctions import addAdyenPaymentForTopUp, add_order, update_order, add_product_order
from first.models import Account, Order, Bakery, HasProduct, Product_order, Product
import datetime
from django.core.exceptions import ObjectDoesNotExist
import hmac
from base64 import b64encode
import hashlib
import json

# CONTSTANTS
MOBILE_SKIN_CODE = 'CDTklqvU'
MOBILE_HMAC_KEY = '186B64CF9623215BAFE622DA227CC5C669EF4C5F09E0632EB9AFA918FD727295'
MOBILE_SKIN_CODE = 'Xvwh5KA0'
MOBILE_HMAC_KEY = '57A6794EFB389EF0ABFC249E54919CDFB7C83BAE6CAFD929E1F8CF6D9358394D'

def getPaymentBill(accountId,bakeryId,orderId,price,shipDateMS,extraCredit,skin):
    import FRG.databaseFunctions as dbf
    try:
        account = Account.objects.get(id = accountId)
        clientPay = price + extraCredit
        succes = 0
        transactionCosts = 0.
        shipDate = datetime.datetime.fromtimestamp(shipDateMS/1000.).date()
        paymentId = dbf.add_AdyenPayment(datetime.datetime.now(),orderId,shipDate,accountId,bakeryId,clientPay,transactionCosts,extraCredit,succes)
        order = Order.objects.get(id = orderId)
        order.status = 'Billed Adyen;' + str(paymentId)
        order.save()
        recurringContract = "RECURRING,ONECLICK"

        if skin == 'mobile':
            skinCode = MOBILE_SKIN_CODE
            key = MOBILE_HMAC_KEY
        else:
            skinCode = NORMAL_SKIN_CODE
            key = NORMAL_HMAC_KEY


        output = {}
        output['shopperEmail'] = account.email
        output['recurringContract'] = recurringContract
        output['shopperReference'] = account.shopperReference
        output['merchantReturnData'] = ''
        output['merchantReference'] = account.firstname + account.lastname + str(paymentId)
        output['skinCode'] = skinCode
        output['currencyCode'] = 'EUR'
        output['paymentAmount'] = price + extraCredit
        output['merchantAccount'] = 'OAKecom'
        output['shopperLocale'] = account.language
        output['shipBeforeDate'] = str(shipDate)
        dummyTime = str(datetime.datetime.now() + datetime.timedelta(hours=2))
        output['sessionValidity'] = dummyTime[:10] + 'T' + dummyTime[11:19] + 'Z'


        signature = str(output['paymentAmount']) + output['currencyCode'] + output['shipBeforeDate'] + \
                    output['merchantReference'] + output['skinCode'] + output['merchantAccount'] + output['sessionValidity'] + \
                    output['shopperEmail'] + output['shopperReference'] + output['recurringContract'] + '' + '' + '' + output['merchantReturnData'] + \
                    '' + '' + '' + ''

        HMAC = getHMAC(signature,key)

        output['merchantSig'] = HMAC

    except ObjectDoesNotExist:
        output = 'accnotfound'

    return output


def getHMAC(signature,key):
    #key = 'f15d5s4f5s7e4fhjk7y5'
    #key = 'Kah942*$7sdp0)' #testkey
    dig = hmac.new(key, msg=signature, digestmod=hashlib.sha1).digest()
    HMAC = b64encode(dig).decode()
    return HMAC

# generates the bill for a credit top up
def getCreditTopUpBill(creditTopUp, skin):
    account = Account.objects.get(id = creditTopUp.accountId)
    paymentId = addAdyenPaymentForTopUp(account,creditTopUp)

    # change status of creditTopUp
    creditTopUp.status = 'Billed Adyen;' + str(paymentId)
    creditTopUp.save()

    recurringContract = "RECURRING,ONECLICK"
    if skin == 'mobile':
        skinCode = MOBILE_SKIN_CODE
        key = MOBILE_HMAC_KEY
    else:
        skinCode = NORMAL_SKIN_CODE
        key = NORMAL_HMAC_KEY


    output = {}
    output['shopperEmail'] = account.email
    output['recurringContract'] = recurringContract
    output['shopperReference'] = account.shopperReference
    output['merchantReturnData'] = 'topUp'
    output['merchantReference'] = account.firstname + account.lastname + str(paymentId)
    output['skinCode'] = skinCode
    output['currencyCode'] = 'EUR'
    output['paymentAmount'] = creditTopUp.amountToPay
    output['merchantAccount'] = 'OAKecom'
    output['shopperLocale'] = account.language
    output['shipBeforeDate'] = str(creditTopUp.dateOrdered)
    dummyTime = str(datetime.datetime.now() + datetime.timedelta(hours=2))
    output['sessionValidity'] = dummyTime[:10] + 'T' + dummyTime[11:19] + 'Z'


    signature = str(output['paymentAmount']) + output['currencyCode'] + output['shipBeforeDate'] + \
                output['merchantReference'] + output['skinCode'] + output['merchantAccount'] + output['sessionValidity'] + \
                output['shopperEmail'] + output['shopperReference'] + output['recurringContract'] + '' + '' + '' + output['merchantReturnData'] + \
                '' + '' + '' + ''

    HMAC = getHMAC(signature,key)

    output['merchantSig'] = HMAC

    return output

# creates a bill to make an adyen payment to top up the credit of an account
def topUpAccountBill(accountId,amountToPay, skin):

    # create CreditTopUp instance
    creditTopUp = bsf.addCreditTopUp(accountId,amountToPay)

    # create the bill
    return getCreditTopUpBill(creditTopUp, skin)


def orderFunction(productArray, accountId, bakeryId, timePickup, comment, task, orderId):
    # makes a new order given the account id, bakery id and a list of products and the amount
    # product array = [[productId,amount],...]
    output = 0
    #check if account exists
    try:
        a = Account.objects.get(id = accountId)
    except ObjectDoesNotExist:
        output = 'accnotfound'
        #check if bakery exists
    try:
        a = Bakery.objects.get(id = bakeryId)
    except ObjectDoesNotExist:
        output = 'Bakery does not exist'
    #check if pickuptime is not in the past
    if datetime.datetime.now() > timePickup:
        output = 'Pickuptime is in the past'

    #check if the bakery has the product
    #safe lists means that if the bakery has all the proudcts it will be 1
    if output == 0:
        totalPrice = 0
        hasProductList = HasProduct.objects.all()
        safe = []
        for i in range(len(productArray)):

            productId = productArray[i]['productId']
            amount = productArray[i]['amount']
            safeValue = 0
            for hasProduct in hasProductList:
                if hasProduct.productId == productId and hasProduct.bakeryId == bakeryId:
                    safeValue = 1
                    totalPrice += hasProduct.price*amount
                    productArray[i]['price'] = hasProduct.price
            safe.append(safeValue)

        if min(safe) != 1:
            output = 'Product not available'


    status = 'new;0'

    if output == 0:
        #if all checks are completed, make the order official and put it in the database
        #TODO: send a mail to the person?
        output = 'success'
        timeOrdered = datetime.datetime.now()
        if task == 'new':
            orderId = add_order(accountId, bakeryId, status, timePickup, timeOrdered, comment,totalPrice)
        if task == 'update':
            #first delete all temporary product_order objects before filling them in again
            product_orders = Product_order.objects.all()
            for product_order in product_orders:
                if product_order.orderId == orderId:
                    product_order.delete()
            #update the order
            update_order(orderId,accountId, bakeryId, status, timePickup, timeOrdered, comment,totalPrice)

        for product in productArray:
            productId = product['productId']
            product_amount = product['amount']
            price = product['price']
            add_product_order(orderId, productId, product_amount,price)

    return output,orderId


def currentOrderPOST(productArray, accountId, bakeryId, timePickupMS, comment):
    try:
        account = Account.objects.get(id = accountId)
        timePickup = datetime.datetime.fromtimestamp(timePickupMS/1000.)
        if account.lastOrderId > 0:
            output,orderId = orderFunction(productArray, accountId, bakeryId, timePickup, comment,'update',account.lastOrderId)
            account.lastOrderId = orderId
            account.save()
        else:
            output,orderId = orderFunction(productArray, accountId, bakeryId, timePickup, comment,'new',0)
            account.lastOrderId = orderId
            account.save()

    except ObjectDoesNotExist:
        output = 'accnotfound'

    return output


def currentOrderGET(accountId):

    account = Account.objects.get(id=accountId)
    orderId = account.lastOrderId
    if not orderId == 0:
        order = Order.objects.get(id=orderId)
        output = {}
        output['accountId'] = order.accountId
        output['status'] = order.status
        output['totalPrice'] = order.totalPrice
        productArray = []
        productOrders = Product_order.objects.all()
        for productOrder in productOrders:
            if productOrder.orderId == orderId:
                tempDict = {}
                tempDict['amount'] = productOrder.amount
                tempDict['price'] = productOrder.price
                tempDict['id'] = productOrder.productId
                product = Product.objects.get(id = productOrder.productId)
                tempDict['name'] = product.name
                tempDict['photoId'] = product.photoId
                productArray.append(tempDict)
        output['products'] = productArray
        output['pickupDate'] = int(order.timePickup.date().strftime("%s")) * 1000

        output['bakery'] = {}
        output['bakery']['id'] = order.bakeryId
        # search for the bakery
        bakery = Bakery.objects.get(id=order.bakeryId)
        output['bakery']['photoId'] = bakery.photoId
        output['bakery']['name'] = bakery.name

        output = json.dumps(output)
    else:
        output = 'nocurrentorder'

    return output


def currentOrderBillCash(accountId,extraCredit,skin):
    account = Account.objects.get(id=accountId)
    orderId = account.lastOrderId
    if orderId > 0:
        order = Order.objects.get(id=orderId)
        shipDate = order.timePickup
        shipDateMS = int(shipDate.date().strftime("%s")) * 1000
        output = getPaymentBill(order.accountId,order.bakeryId,orderId,order.totalPrice,shipDateMS,extraCredit,skin)
        output = json.dumps(output)
    else:
        output = 'nocurrentorder'

    return output


def orderBillCash(orderId,extraCredit,skin):
    try:
        order = Order.objects.get(id=orderId)
        shipDate = order.timePickup
        shipDateMS = int(shipDate.date().strftime("%s")) * 1000
        output = getPaymentBill(order.accountId,order.bakeryId,orderId,order.totalPrice,shipDateMS,extraCredit,skin)

        output = json.dumps(output)
    except ObjectDoesNotExist:
        output = 'orderdoesnotexist'

    return output


def currentOrderBillCredit(accountId):
    account = Account.objects.get(id=accountId)
    orderId = account.lastOrderId
    if orderId > 0:
        order = Order.objects.get(id=orderId)
        output = {}
        output['orderId'] = orderId
        output['credit'] = account.credit
        output['creditAfterPayment'] = account.credit - order.totalPrice
        output = json.dumps(output)
    else:
        output = 'nocurrentorder'

    return output


def orderBillCredit(orderId):
    try:
        order = Order.objects.get(id=orderId)
        account = Account.objects.get(id=order.accountId)
        output = {}
        output['orderId'] = orderId
        output['credit'] = account.credit
        output['creditAfterPayment'] = account.credit - order.totalPrice

        output = json.dumps(output)
    except ObjectDoesNotExist:
        output = 'orderdoesnotexist'

    return output