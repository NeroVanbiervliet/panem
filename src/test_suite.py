#!/usr/bin/env python
# backend test suite
import os
from django.test import Client
import json
import random
import sys
import datetime

# enables standalone execution from command line out of django shell
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panem_project.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

# to perform requests to backend
client = Client()

# ACTIVATED TESTS
t1 = True # 1 TOKEN TESTS
t2 = False # 2 BAKERY TESTS
t3 = False # 3 ORDER TESTS
t4 = False # 4 ACCOUNT TESTS
t5 = False # 5 ME TESTS
t6 = False # 6 ADYEN TESTS
t7 = False # 7 CONTACT TESTS
t8 = False # 8 PROMO CODE TESTS

# COMMON MISTAKES
# http status 301 when doing GET is often because of '/' forgotten at the end of the request

# 
# auxiliary functions
#

# NEED nog auxiliary functions die hierarchisch checken welke error messages er kunnen zijn
# bv. alles onder /bakery/<id>/ en alle suburls hebben zelfde error messages -> zoals token checks :)

# prints an error message to the console in red
def printError(msg): 
	print "\033[0;31m" + msg + "\033[0m "

# prints error if status code not 200 (=OK)
def assertStatusOk(status_code): 
	if(status_code != 200): 
		printError("status not OK: status = " + str(status_code))

# checks if there is a problem with the token
def tokenOk(responseContent): 
	if(responseContent == "tokennotexist"):
		printError(responseContent)
		return False
	elif(responseContent == "tokenexpired"): 
		printError(responseContent)
		return False

	# nothing went wrong
	return True

# saves a html page suite_output.html if the reponse contains html data
def noHtmlError(responseContent):
    if "<html" in responseContent:  # html in response
		f = open('suite_output.html','w')
		f.write(response.content)
		f.close()
		printError("html error written to suite_output.html")
		sys.exit() # terminate script

    return True

#
# 1 TOKEN TESTS
#
if t1:
    print "1 TOKEN TESTS"

    # 1.1 /token/create/ for a guest
    print "1.1 /token/create for a guest"
    request = {
        "email" : "",
        "password" : ""
    }
    response = client.post('/token/create/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    tokenGuest = response.content

    # 1.2 /token/create/ for a normal login
    print "1.2 /token/create for a normal login"
    emailLogin = "nero.vanbiervliet@gmail.com"
    passwordLogin = "rosbeiaard"
    request = {
        "email":emailLogin,
        "password":passwordLogin
    }
    response = client.post('/token/create/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(response.content == "wrongpassword"):
        printError(response.content)
        tokenLogin = "<none>"
    elif(response.content == "accnotfound"):
        printError(response.content)
        tokenLogin = "<none>"
    else:
        tokenLogin = response.content

    # request a token related to a bakery account
    request = {
        "email":"sloewie@gmail.com",
        "password":"rosbeiaard"
    }
    response = client.post('/token/create/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(response.content == "wrongpassword"):
        printError(response.content)
        tokenLoginBakery = "<none>"
    elif(response.content == "accnotfound"):
        printError(response.content)
        tokenLoginBakery = "<none>"
    else:
        tokenLoginBakery = response.content

    # 1.3 /token/verify/
    print "1.3 /token/verify/"
    url = '/token/verify/token=%s/' % tokenLogin
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "valid"):
            if(noHtmlError(response.content)):
                if(response.content != "success"):
                    printError("unknown error : " + response.content)

#
# 2 BAKERY TESTS
#

# constant
bakeryId = 147
if t2:
    print "2 BAKERY TESTS"

    # 2.1 /bakery/
    print "2.1 /bakery/"
    url = '/bakery/token='+tokenLogin+"/"
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)

    # 2.2 /bakery/<id>/offer/
    print "2.2 /bakery/<id>/offer/"
    url = '/bakery/%s/offer/token=%s/' % (bakeryId,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)
    if(response.content == "bakerynotfound"):
        printError(response.content)

    # 2.3 /bakery/<id>/products/
    print "2.3 /bakery/<id>/products/"
    url = '/bakery/%s/products/token=%s/' % (bakeryId,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)
    if(response.content == "bakerynotfound"):
        printError(response.content)

    # 2.4 /bakery/<id>/
    print "2.4 /bakery/<id>/"
    url = '/bakery/%d/token=%s/' % (bakeryId,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)
    if(response.content == "bakerynotfound"):
        printError(response.content)
    # NEED extra output : max aantal dagen vooruit in de toekomst dat bestellingen kunnen gemaakt worden
    # NEED extra output : een array van datums (in ms) waarop de bakker gesloten is, tussen de huidige dag en de bestellimiet (lijntje hier boven)
    # NEED extra output : de zelfde output op de lijn hierboven, maar dan gewoon met integers die aanduiden hoeveel dagen verder dan vandaag de dag is. bv. [0,1,3] zou betekenen : vandaag, morgen en de dag na overmorgen gesloten

    # 2.5 /bakery/search/ with postcode
    print "2.5 /bakery/search/ with postcode"
    postcode = 8310
    url = '/bakery/search/postcode=%s&token=%s/' % (postcode,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)

    # 2.6 /bakery/search/ with longitude and latitude
    print "2.6 /bakery/search/ with longitude and latitude"
    lon = 3.2247000
    lat = 51.2093480
    url = '/bakery/search/GPSLon=%f&GPSLat=%f&token=%s/' % (lon,lat,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)

    # 2.7 /bakery/<id>/products/categories/
    print "2.7 /bakery/<id>/products/categories/"
    url = '/bakery/%d/products/categories/token=%s/' % (bakeryId,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)
    if(response.content == "bakerynotfound"):
        printError(response.content)

    # 2.8 /bakery/<id>/allDayOrders/
    print "2.8 /bakery/<id>/allDayOrders/"
    firstDay = 1462913588554 # may 20, 2016
    lastDay = firstDay - 24*60*60*1000*15 # 15 days earlier
    url = '/bakery/%d/allDayOrders/firstDay=%d&lastDay=%d&token=%s/' % (bakeryId,firstDay,lastDay,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)

    # CHANGEREQUEST in de link kolom in de excel staat er een opmerking na de naam van de endpoint, is die geldig?

    # 2.9 /bakery/<id>/dayOrder/
    print "2.9 /bakery/<id>/dayOrder/"
    dayDate = 1462913588554 # may 20, 2016 TODO interessantere dag
    url = '/bakery/%d/dayOrder/date=%d&token=%s/' % (1000,dayDate,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)

    # 2.10 /bakery/update/
    print "2.10 /bakery/update/"
    request = {
        "token" : tokenLogin,
        "bakeryInfo":{"website":"nero.be","city":"Brugge","name":" Bakkerij Mrs Jackson","taxNumber":"BE123456789","bankAccount":"BE98765432","telephone":"050388453","bestelLimitTime":"17:00","bakerAccountId":53,"member":1,"postcode":8310,"openingHoursString":"[[{\"h\":\"4\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false],[{\"h\":\"6\",\"m\":\"30\"},{\"h\":\"19\",\"m\":\"\"},false]]","adress":"Daverlostraat 192, 8310 Brugge","id":151,"description":"17:00"}
    }

    response = client.post('/bakery/update/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    # 2.11 /bakery/update/emailnotifications
    print "2.11 /bakery/update/emailnotifications/"
    request = {
        "token" : tokenLogin,
        "id":151,
        "emailNotifyNextDayOrder":True
    }

    response = client.post('/bakery/update/emailnotifications/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    # 2.12 /bakery/create/
    print "2.12 /bakery/create/"

    request = {
        "token" : tokenLogin,
        "personInfo" : {
            "firstName"     :   "Phil",
            "lastName"      :   "Lam",
            "email"         :   "louis.vanbiervliet@outlook.com",
            "password"      :   "rosbeiaard",
        },
        "bakeryInfo" : {
            "name"          :   "Bakkermans phillert",
            "address"        :   "Schapenstraat 78",
            #"city"          :   "Leuven",
            #"postcode"      :   "3000",
            "telephone"     :   "0498999336",
            "taxNumber"     :   "TAX3983",
            "bankAccount"   :   "BE46001615257336",
            "openings"      :   ""
        }
    }

    request = {
        "personInfo": {
            "email": "adrisisloewie@gmail.com",
            "password": "rosbeiaard",
            "firstName": "Idris",
            "lastName": "Abidi"
        },
        "bakeryInfo": {
            "name": "pistachenootjes",
            "address": {
                "street": "pistachestraat",
                "postcode": "3000",
                "city": "leuven"
            },
            "telephone": "050310516",
            "taxNumber": "65421",
            "bankAccount": "BE46001615257336"
        },
        "token": tokenLogin
    }

    response = client.post('/bakery/create/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    # 2.13 /bakery/<id>/ingredients/ GET
    print "2.13 /bakery/<id>/ingredients/ GET"
    url = '/bakery/%d/ingredients/token=%s/' % (151,tokenLoginBakery)
    response = client.get(url)
    assertStatusOk(response.status_code)
    tokenOk(response.content)
    if noHtmlError(response.content):
        if (response.content[0] != '{'):
            printError(response.content)

    # 2.14 /bakery/<id>/ingredients/ POST
    print "2.14 /bakery/<id>/ingredients/ POST"
    url = '/bakery/%d/ingredients/' % 151
    request = {
        "token" : tokenLoginBakery,
        "newIngredients":[{'name' : 'caramel'}, {'name' : 'pijnboompitten'}]
    }

    response = client.post(url,content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    # 2.15 /bakery/adaptProducts/ POST
    print "2.15 /bakery/adaptProducts/ POST"
    url = '/bakery/adaptProducts/'
    request = {"token":tokenLoginBakery,"productUpdate":[{"defaultPhotoId":4,"products":[{"available":True,"photoId":1,"name":"Boerenbrood","ingredients":[{"type":"standard","id":26,"name":"ei"},{"type":"standard","id":27,"name":"tarwe"},{"type":"standard","id":30,"name":"aardbeipoeder"},{"type":"custom","id":126,"name":"meelworm"}],"price":0,"id":20,"allergenes":["ei","schaal","tarwe"],"categoryid":1,"$$hashKey":"object:45"},{"available":True,"photoId":1,"name":"Bruin+boerenbrood","ingredients":[{"type":"standard","id":26,"name":"ei"},{"name":"fruitvlieg","type":"custom"}],"price":0,"id":23,"allergenes":["ei","schaal"],"categoryid":1,"$$hashKey":"object:46"},{"available":True,"photoId":1,"name":"Stokbrood","ingredients":[{"name":"fruitvlieg","type":"custom"}],"price":0,"id":30,"allergenes":[],"categoryid":1,"$$hashKey":"object:47"},{"available":False,"photoId":1,"name":"Tijgerbrood","ingredients":[],"price":0,"id":31,"allergenes":[],"categoryid":1,"$$hashKey":"object:48"},{"available":False,"photoId":1,"name":"Volkorenbrood","ingredients":[],"price":0,"id":33,"allergenes":[],"categoryid":1,"$$hashKey":"object:49"},{"available":False,"photoId":1,"name":"Wit+galet","ingredients":[],"price":0,"id":34,"allergenes":[],"categoryid":1,"$$hashKey":"object:50"}],"name":"Broden","id":"1","$$hashKey":"object:37"},{"defaultPhotoId":0,"products":[{"available":False,"photoId":1,"name":"Achtkoek","ingredients":[],"price":0,"id":18,"allergenes":[],"categoryid":3},{"available":False,"photoId":1,"name":"Berlijnse+Bol","ingredients":[],"price":0,"id":19,"allergenes":[],"categoryid":3},{"available":False,"photoId":1,"name":"Boterkoek+met+pudding","ingredients":[],"price":0,"id":21,"allergenes":[],"categoryid":3},{"available":False,"photoId":1,"name":"boterkoek+met+chocoladepudding","ingredients":[],"price":0,"id":22,"allergenes":[],"categoryid":3},{"available":False,"photoId":1,"name":"Lange+suisse","ingredients":[],"price":0,"id":27,"allergenes":[],"categoryid":3},{"available":False,"photoId":1,"name":"Tompoes","ingredients":[],"price":0,"id":32,"allergenes":[],"categoryid":3}],"name":"Klein gebak","id":"3","$$hashKey":"object:38"},{"defaultPhotoId":0,"products":[{"available":False,"photoId":1,"name":"Chocoladekoek","ingredients":[],"price":0,"id":24,"allergenes":[],"categoryid":2},{"available":False,"photoId":1,"name":"Croissant","ingredients":[],"price":0,"id":25,"allergenes":[],"categoryid":2},{"available":False,"photoId":1,"name":"Kleine+Koek","ingredients":[],"price":0,"id":26,"allergenes":[],"categoryid":2},{"available":False,"photoId":1,"name":"Ronde+suisse","ingredients":[],"price":0,"id":28,"allergenes":[],"categoryid":2}],"name":"Koffiekoeken","id":"2","$$hashKey":"object:39"},{"defaultPhotoId":0,"products":[{"available":False,"photoId":1,"name":"Sandwich","ingredients":[],"price":0,"id":29,"allergenes":[],"categoryid":5}],"name":"Broodjes en Pistolets","id":"5","$$hashKey":"object:40"}],"bakeryId":151,"deleteList":[]}

    response = client.post(url,content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    print "NEED remove /bakery/adaptProducts/ POST"
    url = '/bakery/adaptProducts/'
    request = {"token":"1IU1JTVQQD0SQJ","productUpdate":[{"defaultPhotoId":5,"products":[{"available":True,"photoId":5,"name":"Sandwich","ingredients":[{"type":"custom","id":4402,"name":"ei"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4404,"name":"suiker"},{"type":"custom","id":4405,"name":"panda"},{"type":"custom","id":4410,"name":"peper"}],"price":630,"id":9440,"allergenes":[],"categoryid":115,"$$hashKey":"object:47"},{"available":True,"photoId":5,"name":"Picollo","ingredients":[{"type":"custom","id":4406,"name":"geitenkaas"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4407,"name":"meel"},{"type":"custom","id":4404,"name":"suiker"}],"price":822,"id":9441,"allergenes":[],"categoryid":115,"$$hashKey":"object:48"},{"available":True,"photoId":5,"name":"Pistolet","ingredients":[{"type":"custom","id":4406,"name":"geitenkaas"},{"type":"custom","id":4408,"name":"zout"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4404,"name":"suiker"}],"price":268,"id":9442,"allergenes":[],"categoryid":115,"$$hashKey":"object:49"},{"available":True,"photoId":5,"name":"Pistolekke","ingredients":[{"type":"custom","id":4404,"name":"suiker"}],"price":160,"id":9443,"allergenes":[],"categoryid":115,"$$hashKey":"object:50"},{"available":True,"photoId":5,"name":"Brolke","ingredients":[{"type":"custom","id":4412,"name":"bloem"}],"price":160,"id":9444,"allergenes":[],"categoryid":115,"$$hashKey":"object:51"},{"id":"-1","name":"test","photoId":5,"available":True,"price":160,"ingredients":[{"name":"suiker","id":4404,"type":"custom"}],"ingredientsString":"","$$hashKey":"object:67"}],"name":"Broodjes en Pistolets","id":"115","$$hashKey":"object:37"},{"defaultPhotoId":4,"products":[{"available":False,"photoId":4,"name":"Witte Taart","ingredients":[{"type":"custom","id":4409,"name":"rozijnen"},{"type":"custom","id":4410,"name":"peper"}],"price":507,"id":9434,"allergenes":[],"categoryid":114},{"available":True,"photoId":4,"name":"Voetbal Taart","ingredients":[{"type":"custom","id":4411,"name":"melk"}],"price":297,"id":9435,"allergenes":[],"categoryid":114},{"available":True,"photoId":4,"name":"Smurfen Taart","ingredients":[{"type":"custom","id":4412,"name":"bloem"},{"type":"custom","id":4407,"name":"meel"},{"type":"custom","id":4410,"name":"peper"}],"price":166,"id":9436,"allergenes":[],"categoryid":114},{"available":False,"photoId":4,"name":"Aardbei Taart","ingredients":[{"type":"custom","id":4408,"name":"zout"},{"type":"custom","id":4411,"name":"melk"},{"type":"custom","id":4410,"name":"peper"}],"price":637,"id":9437,"allergenes":[],"categoryid":114},{"available":True,"photoId":4,"name":"Framboos Taart","ingredients":[{"type":"custom","id":4402,"name":"ei"},{"type":"custom","id":4404,"name":"suiker"},{"type":"custom","id":4406,"name":"geitenkaas"},{"type":"custom","id":4411,"name":"melk"}],"price":652,"id":9438,"allergenes":[],"categoryid":114},{"available":False,"photoId":4,"name":"Framblij Taart","ingredients":[{"type":"custom","id":4411,"name":"melk"},{"type":"custom","id":4410,"name":"peper"}],"price":906,"id":9439,"allergenes":[],"categoryid":114}],"name":"Taarten","id":"114","$$hashKey":"object:38"},{"defaultPhotoId":1,"products":[{"available":True,"photoId":1,"name":"Wit brood","ingredients":[{"type":"custom","id":4411,"name":"melk"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4405,"name":"panda"},{"type":"custom","id":4405,"name":"panda"},{"type":"custom","id":4413,"name":"chocolade"}],"price":746,"id":9421,"allergenes":[],"categoryid":111},{"available":False,"photoId":1,"name":"Bruin brood","ingredients":[{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4413,"name":"chocolade"}],"price":810,"id":9422,"allergenes":[],"categoryid":111},{"available":True,"photoId":1,"name":"Volkoren brood","ingredients":[{"type":"custom","id":4409,"name":"rozijnen"}],"price":641,"id":9423,"allergenes":[],"categoryid":111},{"available":False,"photoId":1,"name":"Tijger brood","ingredients":[{"type":"custom","id":4410,"name":"peper"},{"type":"custom","id":4404,"name":"suiker"},{"type":"custom","id":4413,"name":"chocolade"},{"type":"custom","id":4409,"name":"rozijnen"}],"price":721,"id":9424,"allergenes":[],"categoryid":111},{"available":True,"photoId":1,"name":"Eerlijk brood","ingredients":[{"type":"custom","id":4414,"name":"water"},{"type":"custom","id":4406,"name":"geitenkaas"}],"price":165,"id":9425,"allergenes":[],"categoryid":111},{"available":True,"photoId":1,"name":"Zwart brood","ingredients":[{"type":"custom","id":4411,"name":"melk"},{"type":"custom","id":4408,"name":"zout"},{"type":"custom","id":4410,"name":"peper"},{"type":"custom","id":4405,"name":"panda"}],"price":810,"id":9426,"allergenes":[],"categoryid":111}],"name":"Broden","id":"111","$$hashKey":"object:39"},{"defaultPhotoId":3,"products":[{"available":False,"photoId":3,"name":"Tompouce","ingredients":[{"type":"custom","id":4412,"name":"bloem"},{"type":"custom","id":4413,"name":"chocolade"},{"type":"custom","id":4411,"name":"melk"}],"price":129,"id":9431,"allergenes":[],"categoryid":113},{"available":False,"photoId":3,"name":"Profiterollekes","ingredients":[{"type":"custom","id":4414,"name":"water"}],"price":847,"id":9432,"allergenes":[],"categoryid":113},{"available":False,"photoId":3,"name":"Muffin","ingredients":[{"type":"custom","id":4406,"name":"geitenkaas"},{"type":"custom","id":4405,"name":"panda"},{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4409,"name":"rozijnen"}],"price":533,"id":9433,"allergenes":[],"categoryid":113}],"name":"Klein gebak","id":"113","$$hashKey":"object:40"},{"defaultPhotoId":2,"products":[{"available":True,"photoId":2,"name":"Croissant","ingredients":[{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4411,"name":"melk"}],"price":191,"id":9427,"allergenes":[],"categoryid":112},{"available":False,"photoId":2,"name":"Chocoladekoek","ingredients":[{"type":"custom","id":4407,"name":"meel"},{"type":"custom","id":4403,"name":"tarwe"}],"price":739,"id":9428,"allergenes":[],"categoryid":112},{"available":False,"photoId":2,"name":"Lange Suisse","ingredients":[{"type":"custom","id":4403,"name":"tarwe"},{"type":"custom","id":4404,"name":"suiker"}],"price":454,"id":9429,"allergenes":[],"categoryid":112},{"available":True,"photoId":2,"name":"Ronde Suisse","ingredients":[{"type":"custom","id":4411,"name":"melk"}],"price":845,"id":9430,"allergenes":[],"categoryid":112}],"name":"Koffiekoeken","id":"112","$$hashKey":"object:41"}],"bakeryId":582,"deleteList":[]}
    response = client.post(url,content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(noHtmlError(response.content)):
            if(response.content != 'success'):
                printError("unknown error : " + response.content)

    # NEED enkele ontbreken

#
# 3 ORDER TESTS
#
if t3:
    print "3 ORDER TESTS"

    # 3.1 /order/current/ POST
    print "3.1 /order/current/ POST"
    # nodig: product_array,account_id,bakery_id,time_pickup,comment,token NEED remove
    today = int(datetime.datetime.now().strftime("%s")) * 1000
    timePickUp = today + 24*60*60*1000*310 # 310 days later
    request = {
        "productArray":[{"productId":1,"amount":4},{"productId":2,"amount":2}],
        "bakeryId":bakeryId,
        "timePickup":timePickUp,
        "remarks":"some remarks on the order",
        "token":tokenLogin
    }
    response = client.post('/order/current/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(not response.content == 'success'):
            printError("unknown error : " + response.content)

    # 3.2 /order/current/ GET
    print "3.2 /order/current/ GET"
    url = '/order/current/token=%s/' % tokenLogin
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(not response.content[0] == "{"):
            printError("unknown error : " + str(response.content))
    # NEED ontbreekt : een array met producten (naam, amount, prijs)
    # NEED het huidige order zou best vernietigd worden na een tijdslimiet, bv 2 uur?

    # 3.3 /order/current/bill/cash/
    print "3.3 /order/current/bill/cash/"
    extraCredit = 1000 # 10 euro
    skin = 'default' # NEED mobile skin ook nog doen
    url = '/order/current/bill/cash/extraCredit=%d&skin=%s&token=%s/' % (extraCredit,skin,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(not response.content[0] == "{"):
            if noHtmlError(response.content):
                if(response.content == "nocurrentorder"):
                    printError(response.content)
                else:
                    printError("unknown error : " + response.content)

    # 3.4 /order/<id>/bill/cash/
    print "3.4 /order/<id>/bill/cash/"
    orderId = 4
    url = '/order/%d/bill/cash/extraCredit=%d&skin=%s&token=%s/' % (orderId,extraCredit,skin,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if noHtmlError(response.content):
            if(response.content[0] != "{"):
                printError("unknown error : " + response.content)

    # 3.5 /order/current/bill/credit/
    print "3.5 /order/current/bill/credit/"
    url = '/order/current/bill/credit/token=%s/' % tokenLogin
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content[0] != "{"):
            printError("unknown error : " + response.content)


    # 3.6 /order/current/receipt/
    print "3.6 /order/current/receipt/"
    request = {
        "token":tokenLogin,
        "merchantReference":"NeroVanbiervliet",
        "skinCode":"randomCode",
        "shopperLocale":"be",
        "paymentMethod":"mc",
        "authResult":"AUTHORISED",
        "pspReference":"somepspid",
        "merchantSig":"234kj34k"
    }
    response = client.post('/order/current/receipt/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content.split('-')[0] != "success"):
            printError("unknown error : " + response.content)

    # 3.7 /order/current/pay/
    print "3.7 /order/current/pay/"
    # first a new order has to be created because the previous has been payed
    request = {
        "productArray":[{"productId":1,"amount":4},{"productId":2,"amount":2}],
        "bakeryId":bakeryId,
        "timePickup":timePickUp,
        "remarks":"some remarks on the order",
        "token":tokenLogin
    }
    response = client.post('/order/current/',content_type='text',data="json=" + json.dumps(request))

    # pay with credits
    request = {
        "token":tokenLogin,
    }
    response = client.post('/order/current/pay/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content.split('-')[0] != "success"):
            if(response.content == "nocurrentorder"):
                printError(response.content)
            else:
                printError("unknown error : " + response.content)

# 
# 4 ACCOUNT TESTS
#
if t4:
    print "4 ACCOUNTS TESTS"

    # 4.1 /account/create/
    print "4.1 /account/create/"
    randEmail = str(random.randint(1e6,1e10)) + '@gmail.com'
    request = {
        "token":tokenLogin,
        "firstname":"nero",
        "lastname":"vanbiervliet",
        "email":randEmail,
        "adress":"leuven",
        "password":"rosbeiaard",
        "type":"normal"
    }
    response = client.post('/account/create/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if(response.content == "alreadyexists"):
                printError(response.content)
            else:
                printError("unknown error : " + response.content)

    # 4.2 /account/verify/
    print "4.2 /account/verify/"
    receivedCode = 0 # TODO niet gekend want email niet ontvangen
    request = {
        "code":receivedCode,
        "email":emailLogin,
        "token":tokenLogin
    }
    response = client.post('/account/verify/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content == "wrongcode" or response.content == "accnotfound" or "alreadyverified"):
            printError(response.content)
        else:
            printError("unknown error : " + response.content)

    # 4.3 /account/verify/resendmail/
    print "4.3 /account/verify/resendmail/"
    url = '/account/verify/resendmail/email=%s&token=%s/' % (randEmail,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if noHtmlError(response.content):
                printError("unknown error : " + response.content)


    # 4.4 /account/password/change/ NEED moven naar /me/password/change
    print "4.4 /account/password/change/"
    newPass = "rosbeiaard"
    request = {
        "token":tokenLogin,
        "email":emailLogin,
        "passwordOriginal":passwordLogin,
        "passwordNew":passwordLogin # can be changed to newPass
    }
    response = client.post('/account/password/change/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if(response.content == "wrongpassword" or response.content == "accnotfound"):
                printError(response.content)
            elif noHtmlError(response.content):
                printError("unknown error : " + response.content)

    # 4.5 /account/password/reset/mail/
    print "4.5 /account/password/reset/mail/"
    request = {
        "token":tokenLogin,
        "email":emailLogin
    }
    # NEED disabled
    # response = client.post('/account/password/reset/mail/', content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if(response.content == "accnotfound"):
                printError(response.content)
            elif noHtmlError(response.content):
                printError("unknown error : " + response.content)

    # 4.6 /account/password/reset/set/
    print "4.6 /account/password/reset/set/"
    request = {
        "token":tokenLogin,
        "passwordNew":passwordLogin,
        "code":"498625"
    }
    # NEED disabled
    # response = client.post('/account/password/reset/set/', content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if(response.content == "accnotfound"):
                printError(response.content)
            elif noHtmlError(response.content):
                printError("unknown error : " + response.content)

#
# 5 ME TESTS
#
if t5:
    print "5 ME TESTS"

    # 5.1 /me/
    print "5.1 /me/"
    url = '/me/token=%s/' % tokenLogin
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(not (response.content[0] == "{")): # no json data returned
            printError("unknown error : " + response.content)

    # CHANGEREQUEST token not authorised (response == 0) zou nooit mogen voorkomen
    # elke token heeft het recht om zijn eigen /me/ op te vragen
    # als het een guest is zit daar ook data, maar niet veel
    # mogelijke data die daar dan kan zitten is bv. welke bakkers er al bezocht zijn door die guest
    # dus wanneer de persoon naar de homepagina navigeert, is er ook al een betere suggestie van bakkers mogelijk door eerder zoekgedrag
    # VRAAG wanneer komt de accnotfound error message voor, ik kan me niet inbeelden wanneer:
    # BAERT: Goed punt, maar dit vergt nog wat meer structurele aanpassingen. accnotfound zou nooit mogen voorkomen, tenzij je een token aanmaakt voor een account die erna wordt verwijderd
    # NEED ook credit toevoegen aan de outputs van dit endpoint
    # NEED indien type=baker dan ook naam van de bakkerij toevoegen aan de outputs

    # 5.2 /me/previousOrders/
    print "5.2 /me/previousOrders/"
    url = '/me/previousOrders/bakeryId=%s&token=%s/' % (bakeryId,tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(not (response.content[0] == "[")): # probably no json data returned
            printError("unknown error : " + response.content)

    # 5.3 /me/topup/bill/
    print "5.3 /me/topup/bill/"
    url = '/me/topup/bill/amount=%d&skin=%s&token=%s/' % (4500,'default',tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            if(response.content == "accnotfound"):
                printError(response.content)
            elif noHtmlError(response.content):
                if not response.content[0] == '{':
                    printError("unknown error : " + response.content)

#
# 6 ADYEN TESTS
#
if t6:
    print "6 ADYEN TESTS"

    # 6.1. adyen/notify/
    print "6.1. adyen/notify/"
    request = {
        "live" : "false",
        "notificationItems" : [
            {
                "NotificationRequestItem" : {

                    "additionalData" : {
                        "authCode" : "58747",
                        "cardSummary" : "1111",
                        "expiryDate" : "6/2016"
                    },

                    "amount" : {
                        "value" : 500,
                        "currency" : "EUR"
                     },

                    "pspReference" : "9313547924770610",
                    "eventCode" : "AUTHORISATION",
                    "eventDate" : "2009-01-01T01:02:01.111+02:00",
                    "merchantAccountCode" : "TestMerchant",

                    "operations" : [
                        "CANCEL",
                        "CAPTURE",
                        "REFUND"
                    ],

                    "merchantReference" : "YourMerchantReference1",
                    "paymentMethod" : "visa",
                    "reason" : "58747:1111:12/2012",
                    "success" : "true"
                }
            }
        ]
    }
    response = client.post('/adyen/notify/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "[accepted]"):
            printError("unknown error : " + response.content)

#
# 7 CONTACT TESTS
#
if t7:
    print "7 CONTACT TESTS"
    # 7.1. contact/
    print "7.1. contact/"
    request = {
        "token" : tokenLogin,
        "name" : "Nero Vanbiervliet",
        "telephone" : "0487244130",
        "email" : "nero.vanbiervliet@gmail.com",
        "paymentReference" : "nerovb123456",
        "question" : "ik kan niet meer inloggen in mijn account. help!"
    }

    response = client.post('/contact/',content_type='text',data="json=" + json.dumps(request))
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "success"):
            printError("unknown error : " + response.content)

    # NEED zeker zijn dat contact met asana gelukt is, anders moet databasefunction een output error geven

#
# 8 PROMO CODE TESTS
#
if t8:
    print "8 PROMO CODE TESTS"
    # 8.1. promo/check/
    print "8.1. promo/check/"
    url = '/promo/check/code=%s&token=%s/' % ('testcode2',tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "valid"):
             printError("unknown error : " + response.content)

    # 8.2. promo/check/
    print "8.2. promo/check/"
    url = '/promo/check/code=%s&token=%s/' % ('testcode1',tokenLogin)
    response = client.get(url)
    assertStatusOk(response.status_code)
    if(tokenOk(response.content)):
        if(response.content != "invalid-used"):
             printError("unknown error : " + response.content)
