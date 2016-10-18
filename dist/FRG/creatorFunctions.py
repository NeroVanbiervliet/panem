from FRG.databaseFunctions import getGpsFromAdress
import FRG.mailHandler as mhl
import GDR.baert_to_split as bts
import GDR.basicFunctions as bsf
from first.models import Bakery, Account
from django.core.exceptions import ObjectDoesNotExist
from base64 import b64encode
import os
import hashlib
import random

def create_bakery(personInfo, bakeryInfo, token):
    #address = bakeryInfo['address'] #+ ' ' + str(bakeryInfo['postcode']) +' '+ bakeryInfo['city']
    address = bakeryInfo['address'] + ' ' + str(bakeryInfo['postcode']) +' '+ bakeryInfo['city']
    GPSLat,GPSLon = getGpsFromAdress(address)

    #Check Of bakker al bestaat
    try:
        object = Bakery.objects.get(taxNumber=bakeryInfo['taxNumber']) # NEED slechte check, want 1 typfoutje leidt tot een nieuwe bakker
        output = 'bakeryalreadyexists'
    except ObjectDoesNotExist:
        #Account Maken

        accountOutput = create_account(personInfo['firstName'], personInfo['lastName'], personInfo['email'], 'baker', address, personInfo['password'],token)

        # Bakker aanmaken
        if accountOutput == 'success':
            accountId = Account.objects.get(email = personInfo['email']).id
            website = ''
            #openingsDefault = '[[{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},0]]'
#            bakeryInfo['postcode'] = 3000
#            bakeryInfo['city'] = ""
            description = 'lolololololololololololololololol'
            bestelLimitTime = '17:00'
            bakeryObject = bsf.add_bakery(bakeryInfo['name'],bakeryInfo['address'],int(bakeryInfo['postcode']),bakeryInfo['city'],GPSLat,GPSLon,bakeryInfo['telephone'],website,bakeryInfo['openings'],description,bestelLimitTime,bakeryInfo['bankAccount'],bakeryInfo['taxNumber'],1,accountId)
            output = 'success'
            #initialise standard products for bakery
            bts.initStandardProducts(bakeryObject)
        else:
            output = 'account' + accountOutput

    return output


def create_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, password,token):

    try:
        #check if the account does not already exists
        account = Account.objects.get(email = emailIn)
        return 'alreadyexists'
    except ObjectDoesNotExist:

        if len(password) < 7:
            return 'passwordtooshort'
        elif not password.isalnum():
            return 'notalphanumeric'
        else:
            salt = b64encode(os.urandom(64)).decode('utf-8')
            passwordSalted = password + salt
            hashed = hashlib.sha512(passwordSalted).hexdigest()
            confirmedNumber = random.randint(1,999999)
            #mhl.sendVerifyMail(emailIn,confirmedNumber,token)
            bsf.add_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, hashed, confirmedNumber,salt)

            return 'success'