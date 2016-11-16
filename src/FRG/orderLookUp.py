from first.models import Order, Product_order, Bakery, Category, Account, Product
import datetime
from django.core.exceptions import ObjectDoesNotExist

# NEED wordt niet gebruikt
def getLastOrdersClient(accountIdIn,N):

    list1 = Order.objects.all()[::-1]
    #inverse order because we want the last orders as last for simplicity in the end
    list2 = Product_order.objects.all()

    output = []

    for order in list1:
        if order.accountId == accountIdIn:
            temp = {}
            temp['date'] = str(order.timePickup.date())
            b = order.timePickup.replace(tzinfo=None).date() - datetime.datetime.now().date()
            temp['NumDaysPast'] = -b.days
            temp['totalPrice'] = order.totalPrice
            temp2 = []
            for product_order in list2:
                if product_order.orderId == order.id:
                    dict1 = {}
                    dict1['productId'] = product_order.productId
                    dict1['amount'] = product_order.amount
                    temp2.append(dict1)

            temp['products'] = temp2

        output.append(temp)

    #here we take the last N elements
    return output[:N]


def get_allDayOrders(bakeryId,firstDay,lastDay):

    try:
        a = Bakery.objects.get(id = bakeryId)

        date1 = datetime.datetime.fromtimestamp(firstDay/1000.).date()
        date2 = datetime.datetime.fromtimestamp(lastDay/1000.).date()
        diff = (date1-date2).days
        diff2 = (datetime.datetime.now().date() - date1).days
        output = []

        for i in range(diff+1):
            dummy = {}
            temp = date1 - datetime.timedelta(i)
            dummy['date'] = int(temp.strftime("%s")) * 1000
            dummy['numDaysPast'] = diff2 + i
            dummy['totalOrders'] = 0
            dummy['totalPrice'] = 0
            dummy['lockState'] = 0
            output.append(dummy)
        orders = Order.objects.all()

        for order in orders:
            datePickup = order.timePickup.replace(tzinfo=None).date()
            if order.bakeryId == bakeryId and datePickup >= date2 and datePickup <= date1:
                index = (date1 - datePickup).days
                output[index]['totalOrders'] += 1
                output[index]['totalPrice'] += order.totalPrice

    except ObjectDoesNotExist:
        output = 'bakerydoesnotexist'

    return output


def get_dayOrder(bakeryId,dateMS):
    date = datetime.datetime.fromtimestamp(dateMS/1000.)

    #check if bakery exists
    try:
        a = Bakery.objects.get(id = bakeryId)

        list1 = Order.objects.all()
        categories = Category.objects.all()
        names = {}
        for category in categories:
            names[str(category.id)] = category.name
        output = {}
        output['date'] = dateMS
        output['totalNumOrders'] = 0
        output['totalMoney'] = 0
        output['orders'] = []
        output['aggregateOrder'] = []
        dummyCategory = []
        dummyName = []
        dummyAmount = []
        dummyId = []

        for order in list1:
            if order.timePickup.replace(tzinfo=None).date()== date.date() and order.bakeryId == bakeryId:
                orderId = order.id
                outputClient = {}
                accountId = order.accountId
                account = Account.objects.get(id = accountId)
                outputClient['firstName'] = account.firstname
                outputClient['lastName'] = account.lastname
                outputClient['products'] = []
                outputClient['totalPrice'] = order.totalPrice
                outputClient['remarks'] = order.comment
                outputClient['isPayed'] = 0 #TODO

                list2 = Product_order.objects.all()
                for productOrder in list2:
                    if productOrder.orderId == orderId:
                        product = Product.objects.get(id=productOrder.productId)
                        productDict = {}
                        productDict['id'] = productOrder.productId
                        productDict['amount'] = productOrder.amount
                        productDict['price'] = productOrder.price
                        productDict['name'] = product.name
                        outputClient['products'].append(productDict)
                        dummyCategory.append(names[str(product.category_id)])
                        dummyName.append(product.name)
                        dummyId.append(productOrder.productId)
                        dummyAmount.append(productOrder.amount)


                output['orders'].append(outputClient)
                output['totalNumOrders'] += 1
                output['totalMoney'] += order.totalPrice

        aggregate = []
        categoryDict = {}
        for category in dummyCategory:
            categoryDict[str(category)] = {}
        nameDict = {}
        for name in dummyName:
            nameDict[str(name)] = {}
            nameDict[str(name)]['amount'] = 0
            nameDict[str(name)]['id'] = 0
            nameDict[str(name)]['name'] = ''

        for i in range(len(dummyName)):
            name = dummyName[i]
            nameDict[str(name)]['name'] = str(name)
            nameDict[str(name)]['amount'] += dummyAmount[i]
            nameDict[str(name)]['id'] = dummyId[i]
            categoryDict[str(dummyCategory[i])][str(name)] = 0

        for key1 in categoryDict:
            tempDict = {}
            tempDict['categoryName'] = key1
            tempDict['products'] = []
            for key2 in categoryDict[key1]:
                tempDict['products'].append(nameDict[key2])

            aggregate.append(tempDict)

        output['aggregateOrder'] = aggregate

    except ObjectDoesNotExist:
        output = 'bakerydoesnotexist'

    return output


def getPreviousOrdersAcrossBakeries(accountId):
    # loop over all bakeries
    objects = Bakery.objects.all()
    output = []
    for bakery in objects:
        currentBakeryOrders = getPreviousOrders(int(accountId),int(bakery.id))
        if currentBakeryOrders != 'ordersnotfound':

            # NEED werkt dit nog?
            # calculate total price for each order with the current prices
            for order in currentBakeryOrders:
                totalPrice = 0
                for product in order['products']:
                    totalPrice += product['amount']*product['price']
                order['totalPrice'] = totalPrice
                # add bakery id to order
                order['bakeryId'] = bakery.id
                order['bakeryName'] = bakery.name

            # add orders to output
            output.extend(currentBakeryOrders)
    return output


def getPreviousOrders(accountId,bakeryId):

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
        output = -'Bakery does not exist'

    if output == 0:
        xSort = []
        output = []
        orders = Order.objects.all()
        productOrders = Product_order.objects.all()

        for order in orders:
            orderTemp = {}
            if order.accountId == accountId and order.bakeryId == bakeryId:
                orderTemp['date'] = int(order.timePickup.date().strftime("%s")) * 1000
                b = order.timePickup.replace(tzinfo=None).date() - datetime.datetime.now().date()
                orderTemp['numDaysPast'] = -b.days
                orderTemp['id'] = order.id
                orderTemp['products'] = []
                for productOrder in productOrders:
                    productDict = {}
                    if productOrder.orderId == order.id:
                        productId = productOrder.productId
                        product = Product.objects.get(id = productId)
                        productDict['price'] = productOrder.price
                        productDict['name'] = product.name
                        productDict['id'] = productId
                        productDict['photoId'] = product.photoId

                        productDict['amount'] = productOrder.amount
                        orderTemp['products'].append(productDict)
                orderTemp['status'] = order.status
                xSort.append(orderTemp['numDaysPast'])
                output.append(orderTemp)
        if len(xSort) > 0:
            xSort, output = zip(*sorted(zip(xSort, output)))
        else:
            output = 'ordersnotfound'

    return output