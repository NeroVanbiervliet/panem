from django.http import HttpResponse
from django.core import serializers
import json
import sys
import urllib
import FRG.authAdministration as atm
import FRG.creatorFunctions as crf
import FRG.mailHandler as mhl
import FRG.orderLookUp as olu
import FRG.salesOffice as slo
import FRG.searchFunctions as srf
import FRG.wareHouse as wrh
import GDR.baert_to_split as bts

sys.path.append("../..")

from FRG import databaseFunctions
import FRG.databaseFunctions as dbf
from GDR import basicFunctions

from first.models import Bakery
from django.core.exceptions import ObjectDoesNotExist

# auxiliary function processing json data
def processJson(request):
    dataToParse = request.body
    # remove json=
    dataToParse = dataToParse.replace('json=','')
    # decode, replaces %7B by {, %22 by ",  %2C by ,
    dataToParse = urllib.unquote(dataToParse)
    # convert + to space
    dataToParse = dataToParse.replace('+',' ')
    # convert to object
    return json.loads(dataToParse)

# auxiliary function checking the request method
def validRequestMethod(request, validMethod):
    if(request.method == validMethod):
        return [True, '']
    else:
        errorMsg =  HttpResponse("This is a " + validMethod + " endpoint. You performed a " + request.method + " request.", status=405) # 405 = method not allowed
        return [False, errorMsg]

# auxiliary function checking if the accountId is associated with a bakery
def isOwner(accountId,bakeryId):
    try:
        bakery = Bakery.objects.get(id=bakeryId)
        if (int(accountId) == int(bakery.bakerAccountId)):
            return True
        else:
            return False
    except ObjectDoesNotExist:
        return False

# shows all information about the bakery object given bakeryId
def bakery(request, bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info
            bakery = databaseFunctions.get_bakery_from_id(int(bakeryId),int(accountId))
            if bakery == 'NA':
                data ='bakerynotfound'
            else:
                #data = serializers.serialize('json', [bakery])
                data = {}
                data['name'] = bakery.name
                data['adress'] = bakery.adress +', '+ str(bakery.postcode) + ' ' + bakery.city 
                data['website'] = bakery.website
                data['openingHours'] = bakery.openings
                data['bestelLimitTime'] = bakery.bestelLimitTime
                data['city'] = bakery.city
                data['postcode'] = bakery.postcode
                data['telephone'] = bakery.telephone
                data['description'] = bakery.description
                data['bankAccount'] = bakery.bankAccount
                data['taxNumber'] = bakery.taxNumber
                data['member'] = bakery.member
                data['bakerAccountId'] = bakery.bakerAccountId
                data['id'] = bakery.id
                data['photoId'] = bakery.photoId
                data['emailNotifyNextDayOrder'] = bakery.emailNotifyNextDayOrder
                data = json.dumps(data)
        else:
            data = info
                
        return HttpResponse(data)

    else:
        return errorMsg
    

# creates a new bakery
def createBakery(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)

        # assign data individual to variables str() necessary because input are unicode type
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        personInfo = {}
        bakeryInfo = {}
        if isinstance(info, int ):
            personInfo['firstName'] = str(parsedData['personInfo']['firstName'])
            personInfo['lastName'] = str(parsedData['personInfo']['lastName'])
            personInfo['email'] = str(parsedData['personInfo']['email'])
            personInfo['password'] = str(parsedData['personInfo']['password'])
            bakeryInfo['name'] = str(parsedData['bakeryInfo']['name'])
            bakeryInfo['address'] = str(parsedData['bakeryInfo']['address'])
            #bakeryInfo['postcode'] = str(parsedData['bakeryInfo']['postcode'])
            #bakeryInfo['city'] = str(parsedData['bakeryInfo']['city'])
            bakeryInfo['telephone'] = str(parsedData['bakeryInfo']['telephone']) 
            bakeryInfo['taxNumber'] = str(parsedData['bakeryInfo']['taxNumber']) 
            bakeryInfo['bankAccount'] = str(parsedData['bakeryInfo']['bankAccount']) 
            #bakeryInfo['openings'] = str(parsedData['bakeryInfo']['openings'])

            output = crf.create_bakery(personInfo, bakeryInfo, token)
        else:
            output = info
        return HttpResponse(str(output))

    else:
        return errorMsg

def adaptBakery(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        # assign data individual to variables str() necessary because input are unicode type
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        bakeryInfo = {}
        if isinstance(info, int ):
            bakeryInfo['id'] = str(parsedData['bakeryInfo']['id'])
            bakeryInfo['name'] = str(parsedData['bakeryInfo']['name'])
            bakeryInfo['description'] = str(parsedData['bakeryInfo']['description'])
            bakeryInfo['adress'] = str(parsedData['bakeryInfo']['adress'])
            bakeryInfo['postcode'] = str(parsedData['bakeryInfo']['postcode'])
            bakeryInfo['city'] = str(parsedData['bakeryInfo']['city'])
            bakeryInfo['telephone'] = str(parsedData['bakeryInfo']['telephone'])
            bakeryInfo['website'] = str(parsedData['bakeryInfo']['website'])
            bakeryInfo['taxNumber'] = str(parsedData['bakeryInfo']['taxNumber']) 
            bakeryInfo['bankAccount'] = str(parsedData['bakeryInfo']['bankAccount']) 
            bakeryInfo['openings'] = str(parsedData['bakeryInfo']['openingHoursString'])
            bakeryInfo['bakerAccountId'] = str(parsedData['bakeryInfo']['bakerAccountId'])
            bakeryInfo['bestelLimitTime'] = str(parsedData['bakeryInfo']['bestelLimitTime'])
            bakeryInfo['member'] = str(parsedData['bakeryInfo']['member'])

            output = databaseFunctions.adapt_bakery(bakeryInfo) 
        else:
            output = info
        return HttpResponse(str(output))

    else:
        return errorMsg
        
# updates the email notification settings for a bakery
# NEED moet eigenlijk fusioneren met adaptBakery
# die functie moet detecteren welke velden er meegegeven worden en dan ook enkel die updaten in de db
def updateEmailNotifications(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        # assign data individual to variables str() necessary because input are unicode type
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        bakeryInfo = {}
        if isinstance(info, int ):
            bakeryInfo['id'] = str(parsedData['id'])
            bakeryInfo['emailNotifyNextDayOrder'] = str(parsedData['emailNotifyNextDayOrder']) == "True" # this is conversion to boolean!

            output = basicFunctions.updateBakeryFlexible(bakeryInfo)
        else:
            output = info

        return HttpResponse(str(output))

    else:
        return errorMsg

def adaptProducts(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        # assign data individual to variables str() necessary because input are unicode type
        token = str(parsedData['token'])
        info = atm.verifyToken(token)

        if isinstance(info, int ):
            bakeryId = str(parsedData['bakeryId'])
            productUpdate = str(parsedData['productUpdate'])
            deleteList = str(parsedData['deleteList'])

            output = wrh.adaptProducts(bakeryId, eval(productUpdate), eval(deleteList))
        else:
            output = info
        return HttpResponse(str(output))

    else:
        return errorMsg
    


def disableDates(request, bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            output = databaseFunctions.get_disableDates(int(bakeryId))
        else:
            output = info
            output = json.dumps(output)
            
        return HttpResponse(output)
    else:
        return errorMsg

#Shows all products of the bakery given bakeryId
def bakeryOffer(request, bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            output1,output2 = databaseFunctions.get_offer_bakery(int(bakeryId))
            if output1 == 'NA':
                data ='bakerynotfound'
            else:
                #data = serializers.serialize('json', [bakery])
                data = [output1,output2]
                data = json.dumps(data)
        else:
            data = info
            
        return HttpResponse(data)

    else:
        return errorMsg

# Shows all products of the bakery given bakeryId
def bakeryProducts(request, bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            output= databaseFunctions.get_products_bakery(int(bakeryId))
            if output == 'NA':
                data ='bakerynotfound'
            else:
                #data = serializers.serialize('json', [bakery])
                data = output
                data = json.dumps(data)
        else:
            data = info
            
        return HttpResponse(data)

    else:
        return errorMsg

# Shows all products sorted per category of the bakery given bakeryId
def bakeryProductsCategories(request, bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
        
            output= databaseFunctions.get_products_category_bakery(int(bakeryId))
            if output == 'NA':
                data ='bakerynotfound'
            else:
                #data = serializers.serialize('json', [bakery])
                data = output
                data = json.dumps(data)
        else:
            data = info
                
        return HttpResponse(data)

    else:
        return errorMsg
        
#Shows all bakeries in database, no inputs
def allBakeries(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):        
            allBakeries = bts.get_all_bakeries()
            data = serializers.serialize('json', allBakeries)
        else:
            data = info
        return HttpResponse(data)

    else:
        return errorMsg

# shows all bakeries with dedicated information for the search function, given longitude and latitude
def bakerySearch(request,GPSLon,GPSLat,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            allBakeries = srf.get_bakery_search(float(GPSLon),float(GPSLat),info)
            #data = serializers.serialize('json', allBakeries)
            data = json.dumps(allBakeries)
        else:
            data = info
        return HttpResponse(data)

    else:
        return errorMsg

# same as bakery search but now postcode is given instead of GPS coordinates
def bakerySearchPostcode(request,postcode,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            allBakeries = srf.get_bakery_search_postcode(int(postcode),info)
            #data = serializers.serialize('json', allBakeries)
            data = json.dumps(allBakeries)
        else:
            data = info
        return HttpResponse(data)

    else:
        return errorMsg
    
# creates account using POST request, given all information needed.
def createAccount(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        # assign data individual to variables str() necessary because input are unicode type
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            firstnameIn = str(parsedData['firstname'])
            lastnameIn = str(parsedData['lastname'])
            emailIn = str(parsedData['email'])
            adressIn = str(parsedData['adress'])
            password = str(parsedData['password'])
            typeIn = str(parsedData['type']) 

            output = crf.create_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, password,token)
        else:
            output = info
        return HttpResponse(str(output))

    else:
        return errorMsg
        
def checkLogin(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)        

        token = str(parsedData['token'])
        emailIn = str(parsedData['email'])
        password = str(parsedData['password'])
        
        info = atm.verifyToken(token)
        if isinstance(info, int ):
        
            output = atm.check_login(emailIn,password)
        else:
            output = info
            
        return HttpResponse(str(output))

    else:
        return errorMsg
   
# verifies the account using the email adress and a code. this endpoint is called from mail
def verifyAccount(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        
        if isinstance(info, int ):
            email = str(parsedData['email'])
            code = str(parsedData['code'])
            output = atm.verify_account(email,code)
        else:
            output = info
            
        return HttpResponse(str(output))

    else:
        return errorMsg

# changes password of the account using POST request given email, new and old password
def changePassword(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        
        token = str(parsedData['token'])
        emailIn = str(parsedData['email'])
        passwordOriginal = str(parsedData['passwordOriginal'])
        passwordNew = str(parsedData['passwordNew'])
        
        info = atm.verifyToken(token)
        if isinstance(info, int ):
        
            output = atm.change_password(emailIn,passwordOriginal,passwordNew)
        else:
            output = info
            
        return HttpResponse(str(output))

    else:
        return errorMsg

def resetPasswordSet(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        token = str(parsedData['token'])
        code = str(parsedData['code'])
        passwordNew = str(parsedData['passwordNew'])

        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info
            output = atm.resetPasswordSet(code,accountId,passwordNew)
            output = json.dumps(output)
        else:
            output = info
    
        return HttpResponse(str(output))

    else:
        return errorMsg

def resetPasswordMail(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)       
        
        emailIn = str(parsedData['email'])
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            output = atm.resetPassword(emailIn,token)
        else:
            output = info

        return HttpResponse(str(output))

    else:
        return errorMsg

# verifies the account using the email adress and a code. this endpoint is called from mail
def repeatVerifyMail(request,emailIn,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):       
            output = mhl.repeatVerifyMail(str(emailIn),str(token))
        else:
            output = info  
        return HttpResponse(output)

    else:
        return errorMsg

# verifies the account using the email adress and a code. this endpoint is called from mail
def allProducts(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):              
            output = databaseFunctions.get_allProducts()
            output = json.dumps(output)
        else:
            output = info
        return HttpResponse(output)

    else:
        return errorMsg

# verifies the account using the email adress and a code. this endpoint is called from mail
def currentOrderGet(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):    
            accountId = info
            output = slo.currentOrderGET(int(accountId))
        else:
            output = info
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(output)

    else:
        return errorMsg
        
def currentOrderPost(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        
        token = str(parsedData['token'])
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):  
            productArray = parsedData['productArray']
            #accountId = request.POST['accountId']
            accountId = info
            bakeryId = parsedData['bakeryId']
            timePickupMS = parsedData['timePickup']
            
            comment = parsedData['remarks']
            output = slo.currentOrderPOST(productArray, int(accountId), int(bakeryId), int(timePickupMS), str(comment))
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(str(output))

    else:
        return errorMsg
        
def currentOrderBillCash(request,extraCredit,skin,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):   
            accountId = info
            output = slo.currentOrderBillCash(int(accountId),int(extraCredit),skin)
            
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(output)

    else:
        return errorMsg
        
def orderBillCash(request,orderId,extraCredit,skin,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            output = slo.orderBillCash(int(orderId),int(extraCredit),skin)
        else:
            output = info
            
        return HttpResponse(output)

    else:
        return errorMsg
        
def currentOrderBillCredit(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):   
            accountId = info
            output = slo.currentOrderBillCredit(int(accountId))
            
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(output)

    else:
        return errorMsg
        
def orderBillCredit(request,orderId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):   
            output = slo.orderBillCredit(int(orderId))
        else:
            output = info
            
        return HttpResponse(output)

    else:
        return errorMsg
        


def currentOrderReceipt(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        
        token = parsedData['token']
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            accountId = info
            merchantReference = parsedData['merchantReference'] 
            authResult = parsedData['authResult']
            output = bts.currentOrderReceipt(str(authResult),int(accountId))
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(str(output))

    else:
        return errorMsg
        
def currentOrderCredit(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        
        token = parsedData['token']
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            accountId = info
            output = bts.currentOrderCredit(accountId)
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(str(output))

    else:
        return errorMsg

def allDayOrders(request,bakeryId,firstDay,lastDay,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):              
            output = olu.get_allDayOrders(int(bakeryId),int(firstDay),int(lastDay))
            output = json.dumps(output)
        else:
            output = info
        return HttpResponse(output)

    else:
        return errorMsg

def dayOrder(request,bakeryId,date,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):              
            output = olu.get_dayOrder(int(bakeryId),int(date))
            output = json.dumps(output)
        else:
            output = info
        return HttpResponse(output)

    else:
        return errorMsg

def previousOrdersAcrossBakeries(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            accountId = info
            output = olu.getPreviousOrdersAcrossBakeries(int(accountId))
            output = json.dumps(output)
        else:
            output = info
        if info == 0:
            output = 'Token not auhorised'
        return HttpResponse(output)

    else:
        return errorMsg

def previousOrders(request,bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            accountId = info
            output = olu.getPreviousOrders(int(accountId),int(bakeryId))
            output = json.dumps(output)
        else:
            output = info
        if info == 0:
            output = 'Token not auhorised'
        return HttpResponse(output)

    else:
        return errorMsg
        
def createToken(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)

        emailIn = str(parsedData['email'])
        password = str(parsedData['password'])
        
        output = atm.createToken(emailIn,password)
        
        return HttpResponse(str(output))

    else:
        return errorMsg
    
def verifyToken(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            output = 'valid'
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
            
        return HttpResponse(output)

    else:
        return errorMsg
        
def token2account(request,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ) and (not info == 0):
            accountId = info
            output = atm.token2account(int(accountId))
            output = json.dumps(output)
        else:
            output = info
            
        if info == 0:
            output = 'tokennotauhorised'
        return HttpResponse(output)

    else:
        return errorMsg

def processAdyenNotification(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        # log event in asana
        databaseFunctions.LogHappenning(1,str(request.body),'test')

        return HttpResponse('[accepted]')

    else:
        return errorMsg

def submitContactIssue(request):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)

        token = parsedData['token']
        name = str(parsedData['name'])
        email = str(parsedData['email'])
        telephone = str(parsedData['telephone'])
        paymentReference = str(parsedData['paymentReference'])
        question = str(parsedData['question'])

        eventText = 'paymentReference : ' + paymentReference + '\nnaam : ' + name + '\nemail : ' + email + '\ntelefoon : ' + telephone + '\nvraag : ' + question

        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info
            databaseFunctions.LogHappenning(accountId,eventText,'contact')
            output = 'success'

        else:
            output = info

        return HttpResponse(output)

    else:
        return errorMsg

# generates the info for an adyen payment to top up the credit
def topUpAccountBill(request,amount,skin,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info
            output = slo.topUpAccountBill(accountId,int(amount), str(skin))
            output = json.dumps(output)

        else:
            output = info

        return HttpResponse(output)

    else:
        return errorMsg

# returns the names of the known ingredients for the current bakery
def getIngredients(request,bakeryId,token):
    [validMethod,errorMsg] = validRequestMethod(request,'GET')

    if validMethod:
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info

            if isOwner(accountId,bakeryId):
                output = wrh.getIngredients(int(bakeryId))
                output = json.dumps(output)

            else:
                output = 'notauthorised' # this can also mean that the bakery does not exist!

        else:
            output = info

        return HttpResponse(output)

    else:
        return errorMsg

# inserts new ingredients for a bakery
def insertIngredients(request,bakeryId):
    [validMethod,errorMsg] = validRequestMethod(request,'POST')

    if validMethod:
        parsedData = processJson(request)
        token = parsedData['token']
        newIngredients = eval(str(parsedData['newIngredients']))
        info = atm.verifyToken(token)
        if isinstance(info, int ):
            accountId = info

            if isOwner(accountId,bakeryId):
                output = wrh.insertIngredients(int(bakeryId),newIngredients)
                if type(output) != type('a string variable '):
                    output = json.dumps(output)

            else:
                output = 'notauthorised' # this can also mean that the bakery does not exist!

        else:
            output = info

        return HttpResponse(output)

    else:
        return errorMsg